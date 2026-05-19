#!/usr/bin/env python3
"""
Create an AgentCore Memory resource for the risk assessment demo.
Run once per AWS account/region. Prints the MEMORY_ID to use.

Usage:
  python scripts/setup-agentcore-memory.py [--region us-east-1]
"""

import argparse
import sys
import time


def main():
    parser = argparse.ArgumentParser(description="Create AgentCore Memory resource")
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--name", default="risk-assessment-memory")
    args = parser.parse_args()

    try:
        from bedrock_agentcore.memory import MemoryClient
    except ImportError:
        print("ERROR: bedrock-agentcore not installed. Run:")
        print("  pip install 'bedrock-agentcore[strands-agents]'")
        sys.exit(1)

    client = MemoryClient(region_name=args.region)

    print(f"Creating AgentCore Memory '{args.name}' in {args.region}...")
    result = client.create_memory(
        name=args.name,
        description="Financial risk assessment multi-agent demo — conversation persistence",
    )

    memory_id = result.get("id") or result.get("memoryId")
    print(f"Memory ID: {memory_id}")
    print(f"Status: {result.get('status', 'CREATING')}")

    print("Waiting for memory to become ACTIVE...")
    for _ in range(30):
        time.sleep(2)
        status = client.get_memory(memory_id=memory_id)
        if status.get("status") == "ACTIVE":
            print(f"Memory is ACTIVE.")
            break
    else:
        print("WARNING: Memory not yet ACTIVE after 60s. Check the console.")

    print(f"\nAdd this to your environment:")
    print(f"  export AGENTCORE_MEMORY_ID={memory_id}")
    print(f"  export AWS_REGION={args.region}")
    print(f"  export MOCK_MODE=false")


if __name__ == "__main__":
    main()
