import type { AgentState, MemoryEvent } from "../types";
import { AGENT_COLORS, AGENT_LABELS } from "../types";

interface Props {
  agents: AgentState[];
  supervisorStatus: "idle" | "active" | "thinking" | "complete";
  supervisorMessage: string;
  memoryEvents: MemoryEvent[];
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    idle: "bg-slate-700 text-slate-400",
    active: "bg-blue-500/20 text-blue-400 border border-blue-500/30",
    thinking: "bg-amber-500/20 text-amber-400 border border-amber-500/30",
    complete: "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30",
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium uppercase tracking-wider ${styles[status] || styles.idle}`}>
      {status}
    </span>
  );
}

function AgentCard({ agent }: { agent: AgentState }) {
  const colors = AGENT_COLORS[agent.name] || AGENT_COLORS.supervisor;
  const isActive = agent.status === "active" || agent.status === "thinking";

  return (
    <div
      className={`rounded-xl border p-3 transition-all duration-500 ${colors.bg} ${
        isActive ? `${colors.border} shadow-lg ${colors.glow}` : "border-slate-800"
      } ${agent.status === "complete" ? `${colors.border}` : ""}`}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <div
            className={`w-2 h-2 rounded-full transition-all ${colors.dot} ${
              isActive ? "animate-pulse-glow" : agent.status === "complete" ? "" : "opacity-30"
            }`}
            style={isActive ? { boxShadow: `0 0 10px currentColor` } : {}}
          />
          <h3 className={`text-sm font-semibold ${isActive || agent.status === "complete" ? colors.text : "text-slate-500"}`}>
            {agent.label}
          </h3>
        </div>
        <StatusBadge status={agent.status} />
      </div>

      {/* Runtime ID */}
      {agent.runtimeId && (
        <div className="mb-2 flex items-center gap-1.5">
          <svg className="w-3 h-3 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2" />
          </svg>
          <span className="font-mono text-[10px] text-slate-600">{agent.runtimeId}</span>
        </div>
      )}

      {/* Tool calls */}
      {agent.toolCalls.length > 0 && (
        <div className="space-y-1.5 mb-2">
          {agent.toolCalls.map((tc, i) => (
            <div key={i} className="animate-slide-in flex items-start gap-2">
              <div className="flex-none mt-1">
                {tc.status === "calling" ? (
                  <div className="w-3 h-3 border border-blue-400 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <svg className="w-3 h-3 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1.5">
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-700/80 text-cyan-400 font-mono">MCP</span>
                  <span className="font-mono text-xs text-slate-300 truncate">{tc.tool}</span>
                </div>
                <p className="font-mono text-[10px] text-slate-600 truncate">{tc.mcpServer}</p>
                {tc.resultPreview && (
                  <p className="text-[10px] text-slate-500 mt-0.5 truncate">{tc.resultPreview}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Result summary */}
      {agent.result && agent.status === "complete" && (
        <div className="animate-fade-in mt-2 pt-2 border-t border-slate-700/50">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-lg font-bold ${colors.text}`}>{agent.result.rating}</span>
            <span className="text-xs text-slate-500">Score: {agent.result.score}/100</span>
          </div>
          {agent.result.key_findings && (
            <ul className="space-y-0.5">
              {agent.result.key_findings.slice(0, 3).map((f, i) => (
                <li key={i} className="text-[11px] text-slate-400 flex items-start gap-1">
                  <span className="text-slate-600 mt-0.5">&#8250;</span>
                  <span>{f}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Status message when active but no tools yet */}
      {agent.status === "thinking" && agent.toolCalls.length > 0 && (
        <p className="text-[11px] text-slate-500 italic">{agent.message}</p>
      )}
    </div>
  );
}

export default function AgentPanel({ agents, supervisorStatus, supervisorMessage, memoryEvents }: Props) {
  const lastMemory = memoryEvents[memoryEvents.length - 1];
  const supervisorColors = AGENT_COLORS.supervisor;

  return (
    <div className="flex flex-col h-full overflow-y-auto">
      <div className="flex-none px-4 py-2.5 border-b border-slate-800 bg-slate-900/40">
        <h2 className="text-sm font-semibold text-slate-300">Agent Activity</h2>
        <p className="text-xs text-slate-500">AgentCore Runtime instances &middot; MCP tool calls &middot; A2A communication</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {/* Memory banner */}
        {lastMemory && (
          <div className="animate-fade-in rounded-lg border border-cyan-500/20 bg-cyan-950/20 px-3 py-2 flex items-center gap-2">
            <svg className="w-4 h-4 text-cyan-500 flex-none" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
            </svg>
            <div className="flex-1 min-w-0">
              <span className="text-[10px] font-semibold text-cyan-400 uppercase tracking-wider">AgentCore Memory</span>
              <p className="text-xs text-slate-400 truncate">
                {lastMemory.action === "retrieve"
                  ? lastMemory.contextSummary
                  : `Stored: ${lastMemory.keysStored?.join(", ")}`}
              </p>
            </div>
            <span className="text-[10px] font-mono text-slate-600">{lastMemory.sessionsCount} sessions</span>
          </div>
        )}

        {/* Supervisor card */}
        <div
          className={`rounded-xl border p-3 transition-all duration-500 ${supervisorColors.bg} ${
            supervisorStatus === "active" || supervisorStatus === "thinking"
              ? `${supervisorColors.border} shadow-lg ${supervisorColors.glow}`
              : supervisorStatus === "complete"
              ? supervisorColors.border
              : "border-slate-800"
          }`}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${supervisorColors.dot} ${
                  supervisorStatus === "active" || supervisorStatus === "thinking"
                    ? "animate-pulse-glow"
                    : supervisorStatus === "idle"
                    ? "opacity-30"
                    : ""
                }`}
              />
              <h3
                className={`text-sm font-semibold ${
                  supervisorStatus !== "idle" ? supervisorColors.text : "text-slate-500"
                }`}
              >
                Supervisor Agent
              </h3>
            </div>
            <StatusBadge status={supervisorStatus} />
          </div>
          {supervisorMessage && (
            <p className="text-xs text-slate-400 mt-1.5">{supervisorMessage}</p>
          )}
        </div>

        {/* Sub-agent grid */}
        <div className="grid grid-cols-2 gap-3">
          {agents.map((agent) => (
            <AgentCard key={agent.name} agent={agent} />
          ))}
        </div>
      </div>
    </div>
  );
}
