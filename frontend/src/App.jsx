import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import PolicySidebar from "./components/PolicySidebar";
import "./App.css";

export default function App() {
  const [prefillQuery, setPrefillQuery] = useState(null);

  return (
    <div className="app-layout">
      <header className="app-header">
        <h1>UHC Policy Assistant</h1>
        <p>AI-powered UnitedHealthcare policy lookup for providers</p>
      </header>
      <div className="app-body">
        <PolicySidebar onSelectPolicy={(q) => setPrefillQuery(q)} />
        <ChatWindow
          prefillQuery={prefillQuery}
          onPrefillConsumed={() => setPrefillQuery(null)}
        />
      </div>
    </div>
  );
}
