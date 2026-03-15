import ReactMarkdown from "react-markdown";
import CitationCard from "./CitationCard";

export default function MessageBubble({ message }) {
  return (
    <div className={`message-bubble ${message.role}`}>
      <div className="message-content">
        {message.role === "assistant" ? (
          <ReactMarkdown>{message.content}</ReactMarkdown>
        ) : (
          <p>{message.content}</p>
        )}
        {message.streaming && <span className="typing-indicator">▊</span>}
      </div>
      {message.citations && message.citations.length > 0 && (
        <div className="citations">
          {message.citations.map((c, i) => (
            <CitationCard key={i} citation={c} />
          ))}
        </div>
      )}
    </div>
  );
}
