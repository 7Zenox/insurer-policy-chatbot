import ReactMarkdown from "react-markdown";
import CitationCard from "./CitationCard";
import { User, Bot } from "lucide-react";

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      {/* Avatar */}
      <div className={`w-7 h-7 rounded-full shrink-0 flex items-center justify-center text-white text-xs
        ${isUser ? "bg-[#3b5f8a]" : "bg-[#1a2e4a]"}`}>
        {isUser ? <User size={14} /> : <Bot size={14} />}
      </div>

      <div className={`flex flex-col gap-2 max-w-[75%] ${isUser ? "items-end" : "items-start"}`}>
        {/* Bubble */}
        <div className={`px-4 py-3 rounded-xl text-sm leading-relaxed
          ${isUser
            ? "bg-[#1a2e4a] text-white rounded-tr-sm"
            : "bg-white border border-[#e5e7eb] text-[#111827] rounded-tl-sm"
          }`}>
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none prose-headings:text-[#1a2e4a] prose-strong:text-[#1a2e4a]">
              <ReactMarkdown>{message.content}</ReactMarkdown>
              {message.streaming && (
                <span className="inline-block w-1.5 h-4 bg-[#3b5f8a] ml-0.5 animate-pulse align-middle" />
              )}
            </div>
          )}
        </div>

        {/* Citations */}
        {message.citations && message.citations.length > 0 && !message.streaming && (
          <div className="flex flex-col gap-1.5 w-full">
            {message.citations.filter(c => c.policy_name && c.policy_name !== "Unknown").map((c, i) => (
              <CitationCard key={i} citation={c} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
