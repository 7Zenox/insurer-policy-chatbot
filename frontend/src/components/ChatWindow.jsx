import { useRef, useEffect, useState } from "react";
import { useSSEChat } from "../hooks/useSSEChat";
import MessageBubble from "./MessageBubble";
import SuggestedQuestions from "./SuggestedQuestions";

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
    <div className="chat-window">
      <div className="message-list">
        {messages.length === 0 && (
          <SuggestedQuestions onSelect={(q) => { sendMessage(q); }} />
        )}
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {isLoading && messages[messages.length - 1]?.role !== "assistant" && (
          <div className="typing-indicator-container">
            <span className="dot-flashing" />
          </div>
        )}
        {error && <div className="error-banner">{error}</div>}
        <div ref={bottomRef} />
      </div>
      <div className="input-bar">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask about UHC policies..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading || !input.trim()}>
          {isLoading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
