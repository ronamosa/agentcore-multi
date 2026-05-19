"""
Market Risk Analyst Agent — Strands SDK
Connects to market_data_mcp via MCPClient for tool calls.
"""

import sys
from pathlib import Path

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.mcp import MCPClient

MCP_SERVER_PATH = str(Path(__file__).resolve().parent.parent / "mcp_servers" / "market_data.py")

SYSTEM_PROMPT = (
    "You are a Market Risk Analyst agent.\n\n"
    "TASK: Use the available MCP tools to gather market and sector data, then produce a risk analysis.\n\n"
    "INSTRUCTIONS:\n"
    "1. Call get_market_conditions with the product_type, and get_sector_exposure with the customer_id.\n"
    "2. Analyze: interest rate environment, sector health, geographic risks, concentration risk.\n"
    "3. Respond with ONLY a JSON object (no markdown fences) with these exact keys:\n"
    '   {"score": <0-100>, "rating": "<letter grade>", "summary": "<one paragraph>", "key_findings": ["...", "..."]}\n'
)


def create_market_analyst(model_id: str = "us.anthropic.claude-haiku-4-5-20250501-v1:0") -> tuple[Agent, MCPClient]:
    mcp_client = MCPClient(
        lambda: stdio_client(StdioServerParameters(command=sys.executable, args=[MCP_SERVER_PATH]))
    )
    model = BedrockModel(model_id=model_id, temperature=0.3, max_tokens=1024)
    agent = Agent(system_prompt=SYSTEM_PROMPT, model=model, tools=[mcp_client])
    return agent, mcp_client
