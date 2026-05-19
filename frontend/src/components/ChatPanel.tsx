import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

interface Props {
  messages: Array<{ role: "user" | "assistant"; content: string }>;
  isRunning: boolean;
  onSend: (query: string) => void;
  customerName?: string;
}

export default function ChatPanel({ messages, isRunning, onSend, customerName }: Props) {
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() && !isRunning) {
      onSend("Perform a full financial risk assessment");
      return;
    }
    if (input.trim() && !isRunning) {
      onSend(input.trim());
      setInput("");
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-none px-4 py-2.5 border-b border-slate-800 bg-slate-900/40">
        <h2 className="text-sm font-semibold text-slate-300">Assessment Chat</h2>
        <p className="text-xs text-slate-500">
          {customerName ? `Assessing ${customerName}` : "Select a customer to begin"}
        </p>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center px-8">
            <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
              </svg>
            </div>
            <p className="text-slate-400 text-sm">Press <b>Enter</b> or click <b>Assess</b> to run a full risk assessment</p>
            <p className="text-slate-600 text-xs mt-1">Or type a specific question about the customer</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`animate-fade-in ${msg.role === "user" ? "flex justify-end" : ""}`}>
            {msg.role === "user" ? (
              <div className="bg-blue-600/20 border border-blue-500/30 rounded-xl rounded-tr-sm px-4 py-2.5 max-w-[85%]">
                <p className="text-sm text-blue-100">{msg.content}</p>
              </div>
            ) : (
              <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl rounded-tl-sm px-4 py-3 max-w-full">
                <div className="text-sm text-slate-200 leading-relaxed prose prose-invert prose-sm max-w-none">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>
            )}
          </div>
        ))}

        {isRunning && messages[messages.length - 1]?.role === "user" && (
          <div className="animate-fade-in flex items-center gap-2 text-slate-500 text-sm">
            <div className="flex gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
            Agents working...
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex-none p-3 border-t border-slate-800">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={customerName ? `Ask about ${customerName}...` : "Select a customer first"}
            disabled={isRunning}
            className="flex-1 bg-slate-800/60 border border-slate-700/60 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500/60 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isRunning}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 text-white text-sm font-medium rounded-lg transition-colors"
          >
            {isRunning ? "Running..." : "Assess"}
          </button>
        </div>
      </form>
    </div>
  );
}
