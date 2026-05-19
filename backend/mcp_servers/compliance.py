"""
MCP Server: Compliance Screening Service
Exposes sanctions checks, PEP screening, and KYC document verification over MCP.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP

import mock_data as data

mcp = FastMCP("compliance_screening_mcp")


@mcp.tool()
def check_sanctions_lists(customer_id: str) -> str:
    """Screen a customer against OFAC, EU, and UN sanctions lists. Returns match status and adverse media hits."""
    result = data.SANCTIONS_CHECK.get(customer_id)
    if not result:
        return json.dumps({"error": f"No sanctions data found for {customer_id}"})
    return json.dumps(result)


@mcp.tool()
def check_pep_status(customer_id: str) -> str:
    """Check whether a customer is a Politically Exposed Person or related to one."""
    result = data.PEP_CHECK.get(customer_id)
    if not result:
        return json.dumps({"error": f"No PEP data found for {customer_id}"})
    return json.dumps(result)


@mcp.tool()
def get_kyc_documents(customer_id: str) -> str:
    """Retrieve KYC document verification status including identity, address, source of funds, and risk category."""
    result = data.KYC_DOCUMENTS.get(customer_id)
    if not result:
        return json.dumps({"error": f"No KYC data found for {customer_id}"})
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()
