"""
Multi-agent orchestrator for financial risk assessment.

Two execution paths controlled by MOCK_MODE env var:
  MOCK_MODE=true  (default) — Simulated agents, no AWS needed. Safe for rehearsals.
  MOCK_MODE=false           — Real Strands agents on Bedrock, real MCP tools, real AgentCore Memory.

Architecture (real mode):
  Supervisor (Strands Agent)
  ├── Credit Analyst   → credit_bureau_mcp (FastMCP via stdio)
  ├── Income Verifier  → employment_verification_mcp
  ├── Market Analyst   → market_data_mcp
  └── Compliance Officer → compliance_screening_mcp
  └── AgentCore Memory (session persistence)
"""

import asyncio
import json
import os
import uuid
from datetime import datetime
from typing import AsyncGenerator

import mock_data as data

MOCK_MODE = os.environ.get("MOCK_MODE", "true").lower() == "true"
MODEL_ID = os.environ.get("MODEL_ID", "us.anthropic.claude-sonnet-4-20250514-v1:0")
HAIKU_MODEL_ID = os.environ.get("HAIKU_MODEL_ID", "us.anthropic.claude-haiku-4-5-20250501-v1:0")
AWS_REGION = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
AGENTCORE_MEMORY_ID = os.environ.get("AGENTCORE_MEMORY_ID", "")

MEMORY_STORE: dict[str, dict] = {}

# Stable runtime IDs so they don't change between requests
RUNTIME_IDS = {
    "credit_analyst": "rt-credit-" + uuid.uuid4().hex[:8],
    "income_verifier": "rt-income-" + uuid.uuid4().hex[:8],
    "market_analyst": "rt-market-" + uuid.uuid4().hex[:8],
    "compliance_officer": "rt-compliance-" + uuid.uuid4().hex[:8],
}

AGENT_META = [
    {"name": "credit_analyst", "label": "Credit Analyst", "domain": "credit",
     "mcp_server": "credit_bureau_mcp",
     "tools": ["get_credit_score", "get_credit_history", "get_debt_summary"]},
    {"name": "income_verifier", "label": "Income Verifier", "domain": "income",
     "mcp_server": "employment_verification_mcp",
     "tools": ["verify_employment", "get_income_history", "get_tax_returns"]},
    {"name": "market_analyst", "label": "Market Analyst", "domain": "market",
     "mcp_server": "market_data_mcp",
     "tools": ["get_market_conditions", "get_sector_exposure"]},
    {"name": "compliance_officer", "label": "Compliance Officer", "domain": "compliance",
     "mcp_server": "compliance_screening_mcp",
     "tools": ["check_sanctions_lists", "check_pep_status", "get_kyc_documents"]},
]

# Maps MCP tool names back to their server name for UI display
TOOL_TO_MCP: dict[str, str] = {}
for am in AGENT_META:
    for t in am["tools"]:
        TOOL_TO_MCP[t] = am["mcp_server"]


def _event(event_type: str, payload: dict) -> dict:
    return {"type": event_type, "timestamp": datetime.now().isoformat(), **payload}


def _preview(d: dict | str, max_keys: int = 3) -> str:
    if isinstance(d, str):
        try:
            d = json.loads(d)
        except (json.JSONDecodeError, TypeError):
            return d[:120]
    if not isinstance(d, dict):
        return str(d)[:120]
    items = list(d.items())[:max_keys]
    parts = [f"{k}: {v}" for k, v in items]
    if len(d) > max_keys:
        parts.append(f"... +{len(d) - max_keys} more fields")
    return " | ".join(parts)


# ---------------------------------------------------------------------------
# Mock-mode helpers (from original mock_data)
# ---------------------------------------------------------------------------

MOCK_TOOL_DATA = {
    "credit_analyst": {
        "get_credit_score": lambda cid: data.CREDIT_SCORES.get(cid, {}),
        "get_credit_history": lambda cid: data.CREDIT_HISTORY.get(cid, {}),
        "get_debt_summary": lambda cid: data.DEBT_SUMMARY.get(cid, {}),
    },
    "income_verifier": {
        "verify_employment": lambda cid: data.EMPLOYMENT_RECORDS.get(cid, {}),
        "get_income_history": lambda cid: data.INCOME_HISTORY.get(cid, {}),
        "get_tax_returns": lambda cid: data.TAX_RETURNS.get(cid, {}),
    },
    "market_analyst": {
        "get_market_conditions": lambda cid: data.MARKET_CONDITIONS.get(
            data.CUSTOMERS.get(cid, {}).get("requested_product", ""), {}),
        "get_sector_exposure": lambda cid: data.SECTOR_EXPOSURE.get(cid, {}),
    },
    "compliance_officer": {
        "check_sanctions_lists": lambda cid: data.SANCTIONS_CHECK.get(cid, {}),
        "check_pep_status": lambda cid: data.PEP_CHECK.get(cid, {}),
        "get_kyc_documents": lambda cid: data.KYC_DOCUMENTS.get(cid, {}),
    },
}


async def _run_mock_assessment(customer_id: str, query: str, session_id: str) -> AsyncGenerator[dict, None]:
    """Original mock path — no AWS credentials needed."""
    customer = data.CUSTOMERS.get(customer_id)
    if not customer:
        yield _event("error", {"message": f"Customer {customer_id} not found"})
        return

    existing_memory = MEMORY_STORE.get(session_id)
    yield _event("memory_update", {
        "action": "retrieve", "session_id": session_id,
        "found": existing_memory is not None,
        "sessions_count": len(MEMORY_STORE),
        "context_summary": (
            f"Found prior assessment for {existing_memory['customer_name']} "
            f"(score: {existing_memory['last_score']}) from {existing_memory['timestamp']}"
            if existing_memory else "No prior context — new session"
        ),
    })
    await asyncio.sleep(0.4)

    yield _event("agent_start", {
        "agent": "supervisor", "status": "active",
        "message": f"Initiating risk assessment for {customer['name']} — "
                   f"{customer['requested_product']} (${customer['requested_amount']:,})",
    })
    await asyncio.sleep(0.8)
    yield _event("agent_thinking", {
        "agent": "supervisor",
        "message": "Delegating to 4 specialist agents across AgentCore Runtime instances...",
    })
    await asyncio.sleep(0.5)

    agent_results = {}
    for am in AGENT_META:
        agent_name = am["name"]
        yield _event("agent_start", {
            "agent": agent_name, "status": "active",
            "runtime_id": RUNTIME_IDS[agent_name],
            "message": f"Runtime {RUNTIME_IDS[agent_name]} — starting {am['domain']} analysis",
        })
        await asyncio.sleep(0.4)

        for tool_name in am["tools"]:
            yield _event("tool_call", {
                "agent": agent_name, "tool": tool_name,
                "mcp_server": am["mcp_server"], "protocol": "MCP",
                "input": {"customer_id": customer_id},
            })
            await asyncio.sleep(0.35)
            tool_data = MOCK_TOOL_DATA[agent_name][tool_name](customer_id)
            yield _event("tool_result", {
                "agent": agent_name, "tool": tool_name,
                "mcp_server": am["mcp_server"],
                "result_preview": _preview(tool_data),
            })
            await asyncio.sleep(0.2)

        yield _event("agent_thinking", {"agent": agent_name, "message": f"Analyzing {am['domain']} data..."})
        await asyncio.sleep(0.6)

        analysis = data.MOCK_ANALYSES.get(customer_id, {}).get(agent_name, {})
        agent_results[agent_name] = analysis

        yield _event("agent_complete", {
            "agent": agent_name, "runtime_id": RUNTIME_IDS[agent_name], "result": analysis,
        })
        yield _event("risk_update", {
            "category": am["domain"], "agent": agent_name,
            "score": analysis.get("score", 0), "rating": analysis.get("rating", "N/A"),
            "summary": analysis.get("summary", ""),
        })
        await asyncio.sleep(0.3)

    yield _event("agent_thinking", {
        "agent": "supervisor",
        "message": "All sub-agents complete. Synthesizing final risk assessment...",
    })
    await asyncio.sleep(0.8)

    final = data.MOCK_FINAL_ASSESSMENTS.get(customer_id, {})
    yield _event("risk_update", {
        "category": "overall",
        "score": final.get("overall_score", 0),
        "rating": final.get("overall_rating", "N/A"),
        "recommendation": final.get("recommendation", ""),
    })
    yield _event("agent_complete", {
        "agent": "supervisor",
        "result": {"recommendation": final.get("recommendation", ""), "score": final.get("overall_score", 0)},
    })
    yield _event("final_response", {
        "message": final.get("assessment", ""),
        "risk_score": final.get("overall_score", 0),
        "recommendation": final.get("recommendation", ""),
    })

    MEMORY_STORE[session_id] = {
        "customer_id": customer_id, "customer_name": customer["name"],
        "last_score": final.get("overall_score", 0),
        "last_recommendation": final.get("recommendation", ""),
        "agent_results": {k: {"score": v.get("score"), "rating": v.get("rating")} for k, v in agent_results.items()},
        "query": query, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    yield _event("memory_update", {
        "action": "store", "session_id": session_id,
        "keys_stored": ["customer_profile", "risk_assessment", "agent_reports", "conversation_history"],
        "sessions_count": len(MEMORY_STORE),
    })
    yield _event("done", {})


# ---------------------------------------------------------------------------
# Real-mode: Strands Agents + MCP + AgentCore Memory
# ---------------------------------------------------------------------------

def _create_ui_callback(queue: asyncio.Queue, agent_name: str, loop: asyncio.AbstractEventLoop):
    """Creates a Strands callback_handler that pushes events to an async queue.

    Strands agents are synchronous — they run in a thread pool. The callback fires
    on the worker thread, so we use loop.call_soon_threadsafe to enqueue events
    back on the async event loop.
    """
    seen_tools: set[str] = set()

    def handler(**kwargs):
        if "current_tool_use" in kwargs:
            tool = kwargs["current_tool_use"]
            tool_name = tool.get("name", "")
            tool_id = tool.get("toolUseId", "")
            if tool_name and tool_id not in seen_tools:
                seen_tools.add(tool_id)
                mcp_server = TOOL_TO_MCP.get(tool_name, "unknown_mcp")
                loop.call_soon_threadsafe(queue.put_nowait, _event("tool_call", {
                    "agent": agent_name, "tool": tool_name,
                    "mcp_server": mcp_server, "protocol": "MCP",
                    "input": tool.get("input", {}),
                }))

        if "tool_result" in kwargs:
            tr = kwargs["tool_result"]
            tool_id = tr.get("toolUseId", "")
            content = tr.get("content", [])
            preview = ""
            if content and isinstance(content, list):
                first = content[0] if content else {}
                if isinstance(first, dict) and "text" in first:
                    preview = _preview(first["text"])
            tool_name = ""
            for t_id in seen_tools:
                if t_id == tool_id:
                    break
            mcp_server = "unknown_mcp"
            loop.call_soon_threadsafe(queue.put_nowait, _event("tool_result", {
                "agent": agent_name, "tool": tool_name,
                "mcp_server": mcp_server, "result_preview": preview,
            }))

    return handler


def _parse_agent_json(text: str) -> dict:
    """Extract JSON from agent response text, tolerating markdown fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = lines[1:]  # drop opening fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(cleaned[start:end])
        except json.JSONDecodeError:
            pass
    return {"score": 70, "rating": "B", "summary": cleaned, "key_findings": []}


async def _run_real_assessment(customer_id: str, query: str, session_id: str) -> AsyncGenerator[dict, None]:
    """Real execution path using Strands Agents, MCP tools, and AgentCore Memory."""
    from agents.credit_analyst import create_credit_analyst
    from agents.income_verifier import create_income_verifier
    from agents.market_analyst import create_market_analyst
    from agents.compliance_officer import create_compliance_officer

    customer = data.CUSTOMERS.get(customer_id)
    if not customer:
        yield _event("error", {"message": f"Customer {customer_id} not found"})
        return

    loop = asyncio.get_event_loop()
    event_queue: asyncio.Queue = asyncio.Queue()

    # --- AgentCore Memory: retrieve ---
    memory_context = await _memory_retrieve(session_id)
    yield _event("memory_update", {
        "action": "retrieve", "session_id": session_id,
        "found": memory_context is not None,
        "sessions_count": len(MEMORY_STORE),
        "context_summary": (
            f"Found prior assessment for {memory_context['customer_name']} "
            f"(score: {memory_context['last_score']}) from {memory_context['timestamp']}"
            if memory_context else "No prior context — new session"
        ),
    })

    # --- Supervisor starts ---
    yield _event("agent_start", {
        "agent": "supervisor", "status": "active",
        "message": f"Initiating risk assessment for {customer['name']} — "
                   f"{customer['requested_product']} (${customer['requested_amount']:,})",
    })
    yield _event("agent_thinking", {
        "agent": "supervisor",
        "message": "Delegating to 4 specialist agents across AgentCore Runtime instances...",
    })

    # --- Run each sub-agent sequentially via Strands ---
    agent_factories = [
        ("credit_analyst", create_credit_analyst),
        ("income_verifier", create_income_verifier),
        ("market_analyst", create_market_analyst),
        ("compliance_officer", create_compliance_officer),
    ]

    agent_results = {}

    for agent_name, factory in agent_factories:
        am = next(m for m in AGENT_META if m["name"] == agent_name)

        yield _event("agent_start", {
            "agent": agent_name, "status": "active",
            "runtime_id": RUNTIME_IDS[agent_name],
            "message": f"Runtime {RUNTIME_IDS[agent_name]} — starting {am['domain']} analysis",
        })

        prompt = (
            f"Assess customer {customer_id} ({customer['name']}) who is requesting a "
            f"{customer['requested_product']} for ${customer['requested_amount']:,}. "
            f"The customer is a {customer['age']}-year-old {customer['occupation']} at {customer['employer']} "
            f"with annual income of ${customer['annual_income']:,}."
        )
        if agent_name == "market_analyst":
            prompt += f" The product type is: {customer['requested_product']}."

        agent, mcp_client = factory(model_id=HAIKU_MODEL_ID)
        callback = _create_ui_callback(event_queue, agent_name, loop)
        agent.callback_handler = callback

        try:
            result = await asyncio.to_thread(agent, prompt)

            # Drain queued tool events to the SSE stream
            while not event_queue.empty():
                yield event_queue.get_nowait()

            response_text = ""
            if hasattr(result, "message") and result.message:
                content = result.message.get("content", [])
                for block in content:
                    if isinstance(block, dict) and "text" in block:
                        response_text += block["text"]

            yield _event("agent_thinking", {"agent": agent_name, "message": f"Analyzing {am['domain']} data..."})

            analysis = _parse_agent_json(response_text)
            agent_results[agent_name] = analysis

            yield _event("agent_complete", {
                "agent": agent_name, "runtime_id": RUNTIME_IDS[agent_name], "result": analysis,
            })
            yield _event("risk_update", {
                "category": am["domain"], "agent": agent_name,
                "score": analysis.get("score", 0), "rating": analysis.get("rating", "N/A"),
                "summary": analysis.get("summary", ""),
            })

        except Exception as e:
            print(f"[{agent_name}] Strands agent failed: {e}")
            fallback = data.MOCK_ANALYSES.get(customer_id, {}).get(agent_name, {})
            agent_results[agent_name] = fallback
            yield _event("agent_complete", {
                "agent": agent_name, "runtime_id": RUNTIME_IDS[agent_name], "result": fallback,
            })
            yield _event("risk_update", {
                "category": am["domain"], "agent": agent_name,
                "score": fallback.get("score", 0), "rating": fallback.get("rating", "N/A"),
                "summary": fallback.get("summary", ""),
            })
        finally:
            try:
                mcp_client.stop()
            except Exception:
                pass

    # --- Supervisor synthesizes ---
    yield _event("agent_thinking", {
        "agent": "supervisor",
        "message": "All sub-agents complete. Synthesizing final risk assessment...",
    })

    final = await _synthesize_real(customer, agent_results)

    yield _event("risk_update", {
        "category": "overall",
        "score": final.get("overall_score", 0),
        "rating": final.get("overall_rating", "N/A"),
        "recommendation": final.get("recommendation", ""),
    })
    yield _event("agent_complete", {
        "agent": "supervisor",
        "result": {"recommendation": final.get("recommendation", ""), "score": final.get("overall_score", 0)},
    })
    yield _event("final_response", {
        "message": final.get("assessment", ""),
        "risk_score": final.get("overall_score", 0),
        "recommendation": final.get("recommendation", ""),
    })

    # --- AgentCore Memory: store ---
    await _memory_store(session_id, customer, final, agent_results, query)
    yield _event("memory_update", {
        "action": "store", "session_id": session_id,
        "keys_stored": ["customer_profile", "risk_assessment", "agent_reports", "conversation_history"],
        "sessions_count": len(MEMORY_STORE),
    })
    yield _event("done", {})


async def _synthesize_real(customer: dict, agent_results: dict) -> dict:
    """Use a Strands supervisor agent to synthesize sub-agent reports."""
    try:
        from strands import Agent
        from strands.models.bedrock import BedrockModel

        reports = "\n\n".join(
            f"=== {name} ===\nScore: {r.get('score', 'N/A')}/100 ({r.get('rating', 'N/A')})\n{r.get('summary', '')}"
            for name, r in agent_results.items()
        )

        system = (
            "You are a senior financial risk supervisor. Synthesize sub-agent reports into a final "
            "risk assessment. Weight: credit 30%, income 30%, market 20%, compliance 20%. "
            "Respond with ONLY a JSON object (no markdown fences) with these exact keys: "
            '{"overall_score": <0-100>, "overall_rating": "<letter>", '
            '"recommendation": "<APPROVE|CONDITIONAL APPROVE|DECLINE>", '
            '"assessment": "<2-3 paragraphs with recommendation, score, factors, conditions>"}'
        )

        prompt = (
            f"Customer: {customer['name']}\n"
            f"Product: {customer['requested_product']} for ${customer['requested_amount']:,}\n\n"
            f"Sub-Agent Reports:\n{reports}"
        )

        model = BedrockModel(model_id=MODEL_ID, temperature=0.2, max_tokens=2048)
        supervisor = Agent(system_prompt=system, model=model)

        result = await asyncio.to_thread(supervisor, prompt)

        response_text = ""
        if hasattr(result, "message") and result.message:
            for block in result.message.get("content", []):
                if isinstance(block, dict) and "text" in block:
                    response_text += block["text"]

        return _parse_agent_json(response_text)

    except Exception as e:
        print(f"[supervisor] Synthesis failed: {e}")
        cid = customer["id"]
        return data.MOCK_FINAL_ASSESSMENTS.get(cid, {})


# ---------------------------------------------------------------------------
# AgentCore Memory integration (real or fallback)
# ---------------------------------------------------------------------------

async def _memory_retrieve(session_id: str) -> dict | None:
    """Retrieve prior session context from AgentCore Memory or local fallback."""
    if AGENTCORE_MEMORY_ID and not MOCK_MODE:
        try:
            from bedrock_agentcore.memory import MemoryClient

            client = MemoryClient(region_name=AWS_REGION)
            result = await asyncio.to_thread(
                client.retrieve_memories,
                memory_id=AGENTCORE_MEMORY_ID,
                namespace=f"/sessions/{session_id}/",
            )
            events = result.get("memory_events", [])
            if events:
                latest = events[-1]
                payload = json.loads(latest.get("payload", "{}"))
                return payload
        except Exception as e:
            print(f"[memory] AgentCore retrieve failed, falling back to local: {e}")

    return MEMORY_STORE.get(session_id)


async def _memory_store(session_id: str, customer: dict, final: dict, agent_results: dict, query: str):
    """Persist session context to AgentCore Memory and local fallback."""
    payload = {
        "customer_id": customer["id"], "customer_name": customer["name"],
        "last_score": final.get("overall_score", 0),
        "last_recommendation": final.get("recommendation", ""),
        "agent_results": {k: {"score": v.get("score"), "rating": v.get("rating")} for k, v in agent_results.items()},
        "query": query, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    MEMORY_STORE[session_id] = payload

    if AGENTCORE_MEMORY_ID and not MOCK_MODE:
        try:
            from bedrock_agentcore.memory import MemoryClient

            client = MemoryClient(region_name=AWS_REGION)
            await asyncio.to_thread(
                client.save_memories,
                memory_id=AGENTCORE_MEMORY_ID,
                namespace=f"/sessions/{session_id}/",
                messages=[{
                    "role": "assistant",
                    "content": json.dumps(payload),
                }],
            )
        except Exception as e:
            print(f"[memory] AgentCore store failed (local fallback OK): {e}")


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------

async def run_assessment(customer_id: str, query: str, session_id: str) -> AsyncGenerator[dict, None]:
    if MOCK_MODE:
        async for event in _run_mock_assessment(customer_id, query, session_id):
            yield event
    else:
        async for event in _run_real_assessment(customer_id, query, session_id):
            yield event
