import { useState, useCallback, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import { BASE_URL } from "../api/client";

export function useSSEChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const sessionId = useRef(uuidv4());

  const sendMessage = useCallback(async (query) => {
    setIsLoading(true);
    setError(null);

    const userMessage = { role: "user", content: query };
    setMessages((prev) => [...prev, userMessage]);

    let assistantContent = "";
    let citations = [];

    setMessages((prev) => [...prev, { role: "assistant", content: "", citations: [], streaming: true }]);

    try {
      const response = await fetch(`${BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, session_id: sessionId.current }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split("\n");

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const event = JSON.parse(line.slice(6));
            if (event.type === "token") {
              assistantContent += event.content;
              setMessages((prev) => {
                const updated = [...prev];
                updated[updated.length - 1] = {
                  role: "assistant",
                  content: assistantContent,
                  citations: [],
                  streaming: true,
                };
                return updated;
              });
            } else if (event.type === "citations") {
              citations = event.sources;
            } else if (event.type === "done") {
              setMessages((prev) => {
                const updated = [...prev];
                updated[updated.length - 1] = {
                  role: "assistant",
                  content: assistantContent,
                  citations,
                  streaming: false,
                };
                return updated;
              });
            } else if (event.type === "error") {
              setError(event.message);
            }
          } catch {}
        }
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  }, [messages.length]);

  return { messages, isLoading, error, sendMessage };
}
