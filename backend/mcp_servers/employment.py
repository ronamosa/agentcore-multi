"""
MCP Server: Employment Verification Service
Exposes employment records, income history, and tax return data over MCP.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP

import mock_data as data

mcp = FastMCP("employment_verification_mcp")


@mcp.tool()
def verify_employment(customer_id: str) -> str:
    """Verify current employment status including employer, title, tenure, and industry."""
    result = data.EMPLOYMENT_RECORDS.get(customer_id)
    if not result:
        return json.dumps({"error": f"No employment record found for {customer_id}"})
    return json.dumps(result)


@mcp.tool()
def get_income_history(customer_id: str) -> str:
    """Retrieve income history, trends, additional income sources, and stability rating."""
    result = data.INCOME_HISTORY.get(customer_id)
    if not result:
        return json.dumps({"error": f"No income history found for {customer_id}"})
    return json.dumps(result)


@mcp.tool()
def get_tax_returns(customer_id: str) -> str:
    """Pull tax return summaries including filing status, AGI, and consistency flags."""
    result = data.TAX_RETURNS.get(customer_id)
    if not result:
        return json.dumps({"error": f"No tax return data found for {customer_id}"})
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()
