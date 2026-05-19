export interface Customer {
  id: string;
  name: string;
  occupation: string;
  requested_product: string;
  requested_amount: number;
}

export type EventType =
  | "agent_start"
  | "agent_thinking"
  | "agent_complete"
  | "tool_call"
  | "tool_result"
  | "memory_update"
  | "risk_update"
  | "final_response"
  | "error"
  | "done";

export interface StreamEvent {
  type: EventType;
  timestamp: string;
  agent?: string;
  status?: string;
  message?: string;
  runtime_id?: string;
  tool?: string;
  mcp_server?: string;
  protocol?: string;
  input?: Record<string, unknown>;
  result?: AgentResult;
  result_preview?: string;
  category?: string;
  score?: number;
  rating?: string;
  summary?: string;
  recommendation?: string;
  risk_score?: number;
  action?: string;
  session_id?: string;
  found?: boolean;
  sessions_count?: number;
  context_summary?: string;
  keys_stored?: string[];
}

export interface AgentResult {
  score?: number;
  rating?: string;
  summary?: string;
  key_findings?: string[];
  recommendation?: string;
}

export interface AgentState {
  name: string;
  label: string;
  status: "idle" | "active" | "thinking" | "complete";
  runtimeId?: string;
  message?: string;
  toolCalls: ToolCall[];
  result?: AgentResult;
}

export interface ToolCall {
  tool: string;
  mcpServer: string;
  status: "calling" | "complete";
  resultPreview?: string;
}

export interface RiskScore {
  category: string;
  score: number;
  rating: string;
  summary?: string;
}

export interface MemoryEvent {
  action: string;
  sessionId?: string;
  found?: boolean;
  sessionsCount: number;
  contextSummary?: string;
  keysStored?: string[];
}

export const AGENT_COLORS: Record<string, { bg: string; border: string; text: string; glow: string; dot: string }> = {
  supervisor: {
    bg: "bg-blue-950/40",
    border: "border-blue-500/40",
    text: "text-blue-400",
    glow: "shadow-blue-500/20",
    dot: "bg-blue-500",
  },
  credit_analyst: {
    bg: "bg-amber-950/40",
    border: "border-amber-500/40",
    text: "text-amber-400",
    glow: "shadow-amber-500/20",
    dot: "bg-amber-500",
  },
  income_verifier: {
    bg: "bg-emerald-950/40",
    border: "border-emerald-500/40",
    text: "text-emerald-400",
    glow: "shadow-emerald-500/20",
    dot: "bg-emerald-500",
  },
  market_analyst: {
    bg: "bg-violet-950/40",
    border: "border-violet-500/40",
    text: "text-violet-400",
    glow: "shadow-violet-500/20",
    dot: "bg-violet-500",
  },
  compliance_officer: {
    bg: "bg-rose-950/40",
    border: "border-rose-500/40",
    text: "text-rose-400",
    glow: "shadow-rose-500/20",
    dot: "bg-rose-500",
  },
};

export const AGENT_LABELS: Record<string, string> = {
  supervisor: "Supervisor",
  credit_analyst: "Credit Analyst",
  income_verifier: "Income Verifier",
  market_analyst: "Market Analyst",
  compliance_officer: "Compliance Officer",
};
