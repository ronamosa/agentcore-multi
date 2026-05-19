"""
FastAPI backend for the AgentCore Financial Risk Assessment demo.
Streams multi-agent events to the React frontend via Server-Sent Events.
"""

import json
import uuid

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

import mock_data as data
from orchestrator import MEMORY_STORE, run_assessment

app = FastAPI(title="AgentCore Risk Assessment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/customers")
async def list_customers():
    return [
        {
            "id": c["id"],
            "name": c["name"],
            "occupation": c["occupation"],
            "requested_product": c["requested_product"],
            "requested_amount": c["requested_amount"],
        }
        for c in data.CUSTOMERS.values()
    ]


@app.get("/api/assess")
async def assess(
    customer_id: str = Query(...),
    query: str = Query(default="Perform a full financial risk assessment"),
    session_id: str = Query(default=None),
):
    if not session_id:
        session_id = str(uuid.uuid4())

    async def event_stream():
        async for event in run_assessment(customer_id, query, session_id):
            yield {"data": json.dumps(event)}

    return EventSourceResponse(event_stream())


@app.get("/api/memory")
async def get_memory():
    return {
        "sessions_count": len(MEMORY_STORE),
        "sessions": [
            {
                "session_id": sid,
                "customer_name": s["customer_name"],
                "last_score": s["last_score"],
                "recommendation": s["last_recommendation"],
                "timestamp": s["timestamp"],
            }
            for sid, s in MEMORY_STORE.items()
        ],
    }


@app.delete("/api/memory")
async def clear_memory():
    MEMORY_STORE.clear()
    return {"status": "cleared"}
