import type { RiskScore } from "../types";

interface Props {
  scores: RiskScore[];
  overallScore: RiskScore | null;
  recommendation: string;
  isRunning: boolean;
}

const CATEGORY_META: Record<string, { label: string; color: string; barColor: string }> = {
  credit: { label: "Credit", color: "text-amber-400", barColor: "bg-amber-500" },
  income: { label: "Income", color: "text-emerald-400", barColor: "bg-emerald-500" },
  market: { label: "Market", color: "text-violet-400", barColor: "bg-violet-500" },
  compliance: { label: "Compliance", color: "text-rose-400", barColor: "bg-rose-500" },
};

function scoreColor(score: number): string {
  if (score >= 80) return "text-emerald-400";
  if (score >= 60) return "text-amber-400";
  return "text-red-400";
}

function scoreBarColor(score: number): string {
  if (score >= 80) return "bg-emerald-500";
  if (score >= 60) return "bg-amber-500";
  return "bg-red-500";
}

function recBadge(rec: string): { bg: string; text: string } {
  if (rec.includes("DECLINE")) return { bg: "bg-red-500/20 border-red-500/40", text: "text-red-400" };
  if (rec.includes("CONDITIONAL")) return { bg: "bg-amber-500/20 border-amber-500/40", text: "text-amber-400" };
  return { bg: "bg-emerald-500/20 border-emerald-500/40", text: "text-emerald-400" };
}

export default function RiskDashboard({ scores, overallScore, recommendation, isRunning }: Props) {
  const hasData = scores.length > 0 || overallScore;
  const badge = recommendation ? recBadge(recommendation) : null;

  return (
    <div className="flex-none border-t border-slate-800 bg-slate-900/60 backdrop-blur-sm px-6 py-3">
      <div className="flex items-center gap-6">
        {/* Overall score */}
        <div className="flex items-center gap-4 flex-none">
          <div className="text-center">
            <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Risk Score</p>
            <div className="flex items-baseline gap-1">
              <span className={`text-3xl font-bold tabular-nums ${overallScore ? scoreColor(overallScore.score) : "text-slate-700"}`}>
                {overallScore ? overallScore.score : "—"}
              </span>
              <span className="text-sm text-slate-600">/100</span>
            </div>
          </div>

          {/* Overall bar */}
          <div className="w-32">
            <div className="h-2.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-1000 ease-out ${
                  overallScore ? scoreBarColor(overallScore.score) : ""
                }`}
                style={{ width: overallScore ? `${overallScore.score}%` : "0%" }}
              />
            </div>
            {overallScore && (
              <p className={`text-xs font-semibold mt-0.5 ${scoreColor(overallScore.score)}`}>
                {overallScore.rating}
              </p>
            )}
          </div>

          {/* Recommendation badge */}
          {badge && recommendation && (
            <div className={`px-3 py-1.5 rounded-lg border ${badge.bg} animate-fade-in`}>
              <span className={`text-xs font-bold ${badge.text}`}>{recommendation}</span>
            </div>
          )}
        </div>

        {/* Separator */}
        <div className="w-px h-10 bg-slate-800 flex-none" />

        {/* Category scores */}
        <div className="flex-1 flex items-center gap-4 overflow-x-auto">
          {Object.entries(CATEGORY_META).map(([key, meta]) => {
            const score = scores.find((s) => s.category === key);
            return (
              <div key={key} className={`flex items-center gap-2 transition-opacity duration-300 ${score ? "" : "opacity-30"}`}>
                <div className="text-center min-w-[60px]">
                  <p className="text-[10px] uppercase tracking-wider text-slate-500">{meta.label}</p>
                  <div className="flex items-baseline justify-center gap-0.5">
                    <span className={`text-lg font-bold tabular-nums ${score ? meta.color : "text-slate-700"}`}>
                      {score ? score.rating : "—"}
                    </span>
                    {score && <span className="text-[10px] text-slate-600">{score.score}</span>}
                  </div>
                </div>
                <div className="w-16">
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-700 ease-out ${meta.barColor}`}
                      style={{ width: score ? `${score.score}%` : "0%" }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Running indicator */}
        {isRunning && (
          <div className="flex-none flex items-center gap-2 text-slate-500">
            <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <span className="text-xs">Assessing...</span>
          </div>
        )}
      </div>
    </div>
  );
}
