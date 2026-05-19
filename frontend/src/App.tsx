import { useCallback, useEffect, useRef, useState } from "react";
import AgentPanel from "./components/AgentPanel";
import ChatPanel from "./components/ChatPanel";
import RiskDashboard from "./components/RiskDashboard";
import type {
  AgentResult,
  AgentState,
  Customer,
  MemoryEvent,
  RiskScore,
  StreamEvent,
} from "./types";
import { AGENT_LABELS } from "./types";

const INITIAL_AGENTS: AgentState[] = [
  { name: "credit_analyst", label: "Credit Analyst", status: "idle", toolCalls: [] },
  { name: "income_verifier", label: "Income Verifier", status: "idle", toolCalls: [] },
  { name: "market_analyst", label: "Market Analyst", status: "idle", toolCalls: [] },
  { name: "compliance_officer", label: "Compliance Officer", status: "idle", toolCalls: [] },
];

export default function App() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState<string>("");
  const [agents, setAgents] = useState<AgentState[]>(INITIAL_AGENTS);
  const [supervisorStatus, setSupervisorStatus] = useState<"idle" | "active" | "thinking" | "complete">("idle");
  const [supervisorMessage, setSupervisorMessage] = useState("");
  const [riskScores, setRiskScores] = useState<RiskScore[]>([]);
  const [overallScore, setOverallScore] = useState<RiskScore | null>(null);
  const [finalResponse, setFinalResponse] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const [memoryEvents, setMemoryEvents] = useState<MemoryEvent[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [chatMessages, setChatMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([]);
  const sessionIdRef = useRef<string>(crypto.randomUUID());

  useEffect(() => {
    fetch("/api/customers")
      .then((r) => r.json())
      .then((data) => {
        setCustomers(data);
        if (data.length > 0) setSelectedCustomer(data[0].id);
      })
      .catch(() => {});
  }, []);

  const resetState = useCallback(() => {
    setAgents(INITIAL_AGENTS.map((a) => ({ ...a, toolCalls: [] })));
    setSupervisorStatus("idle");
    setSupervisorMessage("");
    setRiskScores([]);
    setOverallScore(null);
    setFinalResponse("");
    setRecommendation("");
  }, []);

  const handleEvent = useCallback((event: StreamEvent) => {
    switch (event.type) {
      case "memory_update":
        setMemoryEvents((prev) => [
          ...prev,
          {
            action: event.action || "",
            sessionId: event.session_id,
            found: event.found,
            sessionsCount: event.sessions_count || 0,
            contextSummary: event.context_summary,
            keysStored: event.keys_stored,
          },
        ]);
        break;

      case "agent_start":
        if (event.agent === "supervisor") {
          setSupervisorStatus("active");
          setSupervisorMessage(event.message || "");
        } else {
          setAgents((prev) =>
            prev.map((a) =>
              a.name === event.agent
                ? { ...a, status: "active", runtimeId: event.runtime_id, message: event.message }
                : a
            )
          );
        }
        break;

      case "agent_thinking":
        if (event.agent === "supervisor") {
          setSupervisorStatus("thinking");
          setSupervisorMessage(event.message || "");
        } else {
          setAgents((prev) =>
            prev.map((a) =>
              a.name === event.agent ? { ...a, status: "thinking", message: event.message } : a
            )
          );
        }
        break;

      case "tool_call":
        setAgents((prev) =>
          prev.map((a) =>
            a.name === event.agent
              ? {
                  ...a,
                  toolCalls: [
                    ...a.toolCalls,
                    {
                      tool: event.tool || "",
                      mcpServer: event.mcp_server || "",
                      status: "calling",
                    },
                  ],
                }
              : a
          )
        );
        break;

      case "tool_result":
        setAgents((prev) =>
          prev.map((a) =>
            a.name === event.agent
              ? {
                  ...a,
                  toolCalls: a.toolCalls.map((tc) =>
                    tc.tool === event.tool
                      ? { ...tc, status: "complete" as const, resultPreview: event.result_preview }
                      : tc
                  ),
                }
              : a
          )
        );
        break;

      case "agent_complete":
        if (event.agent === "supervisor") {
          setSupervisorStatus("complete");
        } else {
          setAgents((prev) =>
            prev.map((a) =>
              a.name === event.agent
                ? { ...a, status: "complete", result: event.result as AgentResult }
                : a
            )
          );
        }
        break;

      case "risk_update":
        if (event.category === "overall") {
          setOverallScore({
            category: "overall",
            score: event.score || 0,
            rating: event.rating || "",
          });
          setRecommendation(event.recommendation || "");
        } else {
          setRiskScores((prev) => {
            const exists = prev.find((r) => r.category === event.category);
            if (exists) return prev;
            return [
              ...prev,
              {
                category: event.category || "",
                score: event.score || 0,
                rating: event.rating || "",
                summary: event.summary,
              },
            ];
          });
        }
        break;

      case "final_response":
        setFinalResponse(event.message || "");
        break;

      case "done":
        setIsRunning(false);
        break;
    }
  }, []);

  const runAssessment = useCallback(
    (query?: string) => {
      if (!selectedCustomer || isRunning) return;

      const userMsg = query || "Perform a full financial risk assessment";
      setChatMessages((prev) => [...prev, { role: "user", content: userMsg }]);
      resetState();
      setIsRunning(true);

      const params = new URLSearchParams({
        customer_id: selectedCustomer,
        query: userMsg,
        session_id: sessionIdRef.current,
      });

      const eventSource = new EventSource(`/api/assess?${params}`);

      eventSource.onmessage = (e) => {
        try {
          const event: StreamEvent = JSON.parse(e.data);
          handleEvent(event);

          if (event.type === "final_response") {
            setChatMessages((prev) => [
              ...prev,
              { role: "assistant", content: event.message || "" },
            ]);
          }

          if (event.type === "done") {
            eventSource.close();
          }
        } catch {
          /* ignore parse errors */
        }
      };

      eventSource.onerror = () => {
        eventSource.close();
        setIsRunning(false);
      };
    },
    [selectedCustomer, isRunning, resetState, handleEvent]
  );

  const currentCustomer = customers.find((c) => c.id === selectedCustomer);

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      {/* Header */}
      <header className="flex-none border-b border-slate-800 bg-slate-900/80 backdrop-blur-sm px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div>
              <h1 className="text-lg font-semibold tracking-tight">
                AgentCore <span className="text-slate-500 font-normal">Financial Risk Assessment</span>
              </h1>
              <p className="text-xs text-slate-500">Multi-Agent Orchestration &middot; Runtime &middot; Memory &middot; MCP Tools</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Memory indicator */}
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/50">
              <div className="w-2 h-2 rounded-full bg-cyan-500" style={{ boxShadow: "0 0 8px rgb(6 182 212)" }} />
              <span className="text-xs text-slate-400 font-mono">
                Memory: {memoryEvents.filter((e) => e.action === "store").length} sessions
              </span>
            </div>

            {/* Customer selector */}
            <select
              value={selectedCustomer}
              onChange={(e) => {
                setSelectedCustomer(e.target.value);
                sessionIdRef.current = crypto.randomUUID();
                setMemoryEvents([]);
                setChatMessages([]);
                resetState();
              }}
              className="bg-slate-800 border border-slate-700 text-slate-200 text-sm rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-500"
            >
              {customers.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} — {c.requested_product} (${c.requested_amount.toLocaleString()})
                </option>
              ))}
            </select>
          </div>
        </div>
      </header>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left: Chat panel */}
        <div className="w-[38%] flex flex-col border-r border-slate-800">
          <ChatPanel
            messages={chatMessages}
            isRunning={isRunning}
            onSend={runAssessment}
            customerName={currentCustomer?.name}
          />
        </div>

        {/* Right: Agent activity */}
        <div className="w-[62%] flex flex-col">
          <AgentPanel
            agents={agents}
            supervisorStatus={supervisorStatus}
            supervisorMessage={supervisorMessage}
            memoryEvents={memoryEvents}
          />
        </div>
      </div>

      {/* Bottom: Risk dashboard */}
      <RiskDashboard
        scores={riskScores}
        overallScore={overallScore}
        recommendation={recommendation}
        isRunning={isRunning}
      />
    </div>
  );
}
