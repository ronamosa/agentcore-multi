"""
MCP Server: Market Data Service
Exposes market conditions and sector exposure data over MCP.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP

import mock_data as data

mcp = FastMCP("market_data_mcp")


@mcp.tool()
def get_market_conditions(product_type: str) -> str:
    """Get current market conditions for a loan product type (e.g. Mortgage, Business Expansion Loan, Auto Loan)."""
    result = data.MARKET_CONDITIONS.get(product_type)
    if not result:
        return json.dumps({"error": f"No market data found for product type '{product_type}'"})
    return json.dumps(result)


@mcp.tool()
def get_sector_exposure(customer_id: str) -> str:
    """Analyze sector and geographic exposure for a customer including concentration risk."""
    result = data.SECTOR_EXPOSURE.get(customer_id)
    if not result:
        return json.dumps({"error": f"No sector exposure data found for {customer_id}"})
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()
