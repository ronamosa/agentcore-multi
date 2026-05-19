"""
Compliance Officer Agent — Strands SDK
Connects to compliance_screening_mcp via MCPClient for tool calls.
"""

import sys
from pathlib import Path

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.mcp import MCPClient

MCP_SERVER_PATH = str(Path(__file__).resolve().parent.parent / "mcp_servers" / "compliance.py")

SYSTEM_PROMPT = (
    "You are a Compliance Officer agent responsible for KYC/AML screening.\n\n"
    "TASK: Use the available MCP tools to run compliance checks, then produce a risk analysis.\n\n"
    "INSTRUCTIONS:\n"
    "1. Call check_sanctions_lists, check_pep_status, and get_kyc_documents for the customer_id provided.\n"
    "2. Analyze: sanctions matches, PEP status, adverse media, KYC document completeness, EDD requirements.\n"
    "3. Respond with ONLY a JSON object (no markdown fences) with these exact keys:\n"
    '   {"score": <0-100>, "rating": "<letter grade>", "summary": "<one paragraph>", "key_findings": ["...", "..."]}\n'
)


def create_compliance_officer(model_id: str = "us.anthropic.claude-haiku-4-5-20250501-v1:0") -> tuple[Agent, MCPClient]:
    mcp_client = MCPClient(
        lambda: stdio_client(StdioServerParameters(command=sys.executable, args=[MCP_SERVER_PATH]))
    )
    model = BedrockModel(model_id=model_id, temperature=0.3, max_tokens=1024)
    agent = Agent(system_prompt=SYSTEM_PROMPT, model=model, tools=[mcp_client])
    return agent, mcp_client
