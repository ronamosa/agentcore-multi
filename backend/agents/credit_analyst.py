"""
Credit Analyst Agent — Strands SDK
Connects to credit_bureau_mcp via MCPClient for tool calls.
"""

import sys
from pathlib import Path

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.mcp import MCPClient

MCP_SERVER_PATH = str(Path(__file__).resolve().parent.parent / "mcp_servers" / "credit_bureau.py")

SYSTEM_PROMPT = (
    "You are a Credit Analyst agent specializing in consumer and commercial credit risk assessment.\n\n"
    "TASK: Use the available MCP tools to gather credit data for the given customer, then produce a risk analysis.\n\n"
    "INSTRUCTIONS:\n"
    "1. Call get_credit_score, get_credit_history, and get_debt_summary for the customer_id provided.\n"
    "2. Analyze: credit score, utilization, payment history, DTI ratio, derogatory marks.\n"
    "3. Respond with ONLY a JSON object (no markdown fences) with these exact keys:\n"
    '   {"score": <0-100>, "rating": "<letter grade>", "summary": "<one paragraph>", "key_findings": ["...", "..."]}\n'
)


def create_credit_analyst(model_id: str = "us.anthropic.claude-haiku-4-5-20250501-v1:0") -> tuple[Agent, MCPClient]:
    """Create and return (agent, mcp_client). Caller manages MCP lifecycle."""
    mcp_client = MCPClient(
        lambda: stdio_client(StdioServerParameters(command=sys.executable, args=[MCP_SERVER_PATH]))
    )
    model = BedrockModel(model_id=model_id, temperature=0.3, max_tokens=1024)
    agent = Agent(system_prompt=SYSTEM_PROMPT, model=model, tools=[mcp_client])
    return agent, mcp_client
