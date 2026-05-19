# Demo Script -- AgentCore Financial Risk Assessment

Total time: ~4-5 minutes (with patter). Can compress to 3 min if tight.

---

## Before you start

1. Have two terminals open but hidden: backend (`make mock` or `make real`) and frontend (`cd frontend && npm run dev`).
2. Browser open to `http://localhost:5173` -- dark theme, no data yet.
3. If running real mode, confirm `MOCK_MODE=false` and AWS credentials are working.
4. Clear any prior sessions: click the customer dropdown to reset state.

---

## Opening (30 seconds)

> "I'm going to show you how Amazon Bedrock AgentCore lets you build multi-agent systems that are actually production-ready -- not just a notebook demo. We'll see three AgentCore capabilities in action: **Runtime**, **Memory**, and **MCP tool use**."
>
> "The use case is financial risk assessment. A customer walks in wanting a loan. Instead of one monolithic model, we have a **team of specialist agents** -- each with its own expertise, its own tools, and its own runtime."

---

## Part 1 -- Agent Runtime + MCP Tools (2 minutes)

### What you do

1. **Customer dropdown** is already set to **Sarah Chen -- Mortgage ($750,000)**.
2. Click **Assess** (or press Enter).

### What the audience sees

- The **Supervisor Agent** card lights up blue -- "Initiating risk assessment..."
- It delegates to 4 specialist agents. Each one activates in sequence.

### Talk track as agents activate

> "The supervisor is coordinating four specialist agents. Each one runs in its own AgentCore Runtime -- isolated, independently scalable."

**Credit Analyst lights up (amber):**
> "The Credit Analyst is now calling MCP tools -- you can see the tool calls streaming in. `get_credit_score` from the credit bureau MCP server, `get_credit_history`, `get_debt_summary`. These are real MCP protocol calls -- the same Model Context Protocol that's becoming the standard for agent-tool communication."

Point to the `MCP` badges and tool names as they appear.

> "Each tool call hits a FastMCP server. In production these would be wrappers around your actual credit bureau APIs, your Equifax integration, whatever. The MCP layer makes the tools discoverable and self-describing."

**Income Verifier lights up (green):**
> "Income verification -- checking employment records, income history, tax returns. Different MCP server, different domain."

**Market Analyst lights up (purple):**
> "Market conditions -- interest rates, sector exposure, geographic risk."

**Compliance Officer lights up (red/rose):**
> "And compliance -- sanctions screening, PEP checks, KYC documents. Four agents, four MCP servers, eleven total tool calls."

### When results come in

As each agent completes, point to the **risk dashboard at the bottom**:

> "As each agent finishes, their risk score feeds into the dashboard. Credit: B+, Income: A, Market: B-, Compliance: A+."

When the supervisor synthesizes:

> "Now the supervisor takes all four reports and synthesizes a final assessment. Score: 82 out of 100. Recommendation: APPROVE."

Point to the chat panel where the full assessment appears:

> "Sarah Chen is a strong candidate -- high income, low DTI, clean compliance. The only flag is geographic concentration in the Bay Area tech market."

### Key point

> "What you just saw: **five Strands agents** running against **Bedrock**, each calling **real MCP tools**, all coordinated through the agents-as-tools pattern. This is the same code that deploys to AgentCore Runtime containers."

---

## Part 2 -- Contrast with a riskier customer (1 minute)

### What you do

1. Switch the dropdown to **Marcus Rivera -- Business Expansion Loan ($250,000)**.
2. Click **Assess**.

### Talk track

> "Let's see how the system handles a riskier profile. Marcus is a restaurant owner, 3 years in, wants $250K to expand."

As agents work:

> "Same agent team, same MCP tools, completely different data flowing through."

When results land:

> "Very different picture. Credit: C+, high utilization, recent late payments. Income: C+, volatile self-employment. Market: D+, restaurant industry has a 60% five-year failure rate. Score: 56. CONDITIONAL APPROVE -- the system recommends reducing the loan amount and requiring quarterly financials."

> "Same infrastructure, same agents -- but the risk assessment adapts completely to the customer profile."

---

## Part 3 -- AgentCore Memory (45 seconds)

### What you do

1. Stay on **Marcus Rivera**.
2. Click **Assess** again (second time, same customer).

### What the audience sees

- The **Memory banner** (cyan, top of agent panel) now shows: "Found prior assessment for Marcus Rivera (score: 56)".
- The session count increments.

### Talk track

> "Here's where AgentCore Memory comes in. See the cyan banner at the top? The system retrieved Marcus's prior assessment from memory. It knows we already scored him at 56."

> "In a real system, this means your agents have **persistent context**. A customer calls back, asks a follow-up question, the agents don't start from scratch. AgentCore Memory handles session persistence -- short-term within a conversation, long-term across sessions."

Point to the memory indicator in the header:

> "Two sessions stored now. This uses the AgentCore Memory SDK -- the same API whether you're running locally or deployed to Runtime."

---

## Part 4 (optional) -- Emily Watson (30 seconds)

If you have time:

1. Switch to **Emily Watson -- Auto Loan ($35,000)**.
2. Assess.

> "One more -- a thin credit file, early career. Score: 72. Approved, but with conditions. The system flags the short credit history and limited income track record."

---

## Closing (30 seconds)

> "To recap what you saw:"
>
> "**AgentCore Runtime** -- five agents, each a Strands Agent with its own Bedrock model, running in isolated runtime contexts."
>
> "**MCP Tools** -- eleven tool calls across four FastMCP servers. Real protocol, real tool discovery, real data flow."
>
> "**AgentCore Memory** -- session context that persists across interactions. The agents remember."
>
> "This is all open source, built on Strands Agents SDK, deployable with `cdk deploy`. The code running in this demo is the same code that runs in production AgentCore Runtime containers."

---

## If someone asks...

**"Is the data real?"**
> "The data is mock -- realistic financial profiles but not from a real bureau. In production, the MCP servers would wrap your actual data APIs. The MCP layer and agent logic are identical either way."

**"How long do real Bedrock calls take?"**
> "In real mode with actual Bedrock calls, each agent takes 3-5 seconds (Haiku is fast). The full assessment runs in about 20-30 seconds. Mock mode is instant for rehearsals."

**"Can the agents run in parallel?"**
> "Yes -- the agents-as-tools pattern supports parallel execution. We run them sequentially here so the audience can see each one activate. In production you'd parallelize for throughput."

**"What about the UI -- is that deployed too?"**
> "The React frontend connects via SSE (Server-Sent Events). In production you'd deploy it behind CloudFront. The backend is a FastAPI server that can run in a container or Lambda."

**"How does this compare to Bedrock Agents (the managed service)?"**
> "Bedrock Agents is fully managed -- you configure agents in the console. AgentCore gives you more control -- you write the agent code with Strands SDK, deploy your own containers, wire up your own tools via MCP. More flexibility, more code, same Bedrock models underneath."

---

## Troubleshooting during the demo

| Problem | Fix |
|---------|-----|
| Backend not responding | Check terminal: `make mock` (or `make real`) should show Uvicorn running on :8000 |
| Frontend blank | Check terminal: `cd frontend && npm run dev` should show Vite on :5173 |
| SSE stream hangs | Refresh the browser. If persistent, restart the backend |
| Real mode errors | Check AWS credentials: `aws sts get-caller-identity`. Ensure Bedrock model access is enabled in your region |
| Memory not showing | Memory persists in-process. If you restarted the backend, prior sessions are gone (expected for mock mode) |
