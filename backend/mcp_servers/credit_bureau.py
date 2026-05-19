"""
MCP Server: Credit Bureau Service
Exposes credit score, history, and debt data over the Model Context Protocol.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP

import mock_data as data

mcp = FastMCP("credit_bureau_mcp")


@mcp.tool()
def get_credit_score(customer_id: str) -> str:
    """Retrieve the credit score and rating band for a customer from the credit bureau."""
    result = data.CREDIT_SCORES.get(customer_id)
    if not result:
        return json.dumps({"error": f"No credit score found for {customer_id}"})
    return json.dumps(result)


@mcp.tool()
def get_credit_history(customer_id: str) -> str:
    """Pull the full credit history report including accounts, utilization, payment history, and derogatory marks."""
    result = data.CREDIT_HISTORY.get(customer_id)
    if not result:
        return json.dumps({"error": f"No credit history found for {customer_id}"})
    return json.dumps(result)


@mcp.tool()
def get_debt_summary(customer_id: str) -> str:
    """Get current debt obligations breakdown including total debt, monthly payments, DTI ratio, and per-account details."""
    result = data.DEBT_SUMMARY.get(customer_id)
    if not result:
        return json.dumps({"error": f"No debt summary found for {customer_id}"})
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()
