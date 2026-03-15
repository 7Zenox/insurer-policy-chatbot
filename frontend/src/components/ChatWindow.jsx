import { useRef, useEffect, useState } from "react";
import { useSSEChat } from "../hooks/useSSEChat";
import MessageBubble from "./MessageBubble";
import SuggestedQuestions from "./SuggestedQuestions";
import { Send } from "lucide-react";

export default function ChatWindow({ prefillQuery, onPrefillConsumed }) {
  const { messages, isLoading, error, sendMessage } = useSSEChat();
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    if (prefillQuery) {
      setInput(prefillQuery);
      onPrefillConsumed?.();
    }
  }, [prefillQuery]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    sendMessage(input.trim());
    setInput("");
  };

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      {/* Chat header */}
      <div className="bg-white border-b border-[#e5e7eb] px-6 py-3 shrink-0">
        <div className="text-[#1a2e4a] font-semibold text-sm">Policy Assistant</div>
        <div className="text-[#6b7280] text-xs mt-0.5">Ask questions about UHC commercial medical and drug policies</div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 flex flex-col gap-4">
        {messages.length === 0 && (
          <SuggestedQuestions onSelect={(q) => sendMessage(q)} />
        )}
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {isLoading && messages[messages.length - 1]?.role !== "assistant" && (
          <div className="flex items-center gap-2 text-[#6b7280] text-sm">
            <div className="flex gap-1">
              <span className="w-1.5 h-1.5 bg-[#3b5f8a] rounded-full animate-bounce [animation-delay:0ms]" />
              <span className="w-1.5 h-1.5 bg-[#3b5f8a] rounded-full animate-bounce [animation-delay:150ms]" />
              <span className="w-1.5 h-1.5 bg-[#3b5f8a] rounded-full animate-bounce [animation-delay:300ms]" />
            </div>
            <span>Searching policies...</span>
          </div>
        )}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-2 rounded">
            {error}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-[#e5e7eb] px-6 py-4 shrink-0">
        <div className="flex gap-2 items-end">
          <textarea
            rows={1}
            value={input}
            onChange={(e) => {
              setInput(e.target.value);
              e.target.style.height = "auto";
              e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Ask about coverage, prior auth, CPT codes..."
            disabled={isLoading}
            className="flex-1 resize-none border border-[#e5e7eb] rounded-lg px-4 py-2.5 text-sm text-[#111827] placeholder-[#9ca3af] focus:outline-none focus:border-[#3b5f8a] focus:ring-1 focus:ring-[#3b5f8a] disabled:opacity-50 bg-[#f9fafb]"
            style={{ minHeight: "42px" }}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="bg-[#1a2e4a] hover:bg-[#3b5f8a] disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-lg p-2.5 transition-colors shrink-0"
          >
            <Send size={16} />
          </button>
        </div>
        <div className="text-[#9ca3af] text-xs mt-2">Press Enter to send · Shift+Enter for new line</div>
      </div>
    </div>
  );
}
