import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import PolicySidebar from "./components/PolicySidebar";

export default function App() {
  const [prefillQuery, setPrefillQuery] = useState(null);

  return (
    <div className="flex flex-col h-screen bg-[#f3f4f6]">
      {/* Top Nav */}
      <header className="bg-[#1a2e4a] px-6 py-3 flex items-center gap-3 shrink-0">
        <div className="w-8 h-8 bg-[#3b5f8a] rounded flex items-center justify-center">
          <span className="text-white text-sm font-bold">C</span>
        </div>
        <div>
          <div className="text-white font-semibold text-base leading-tight">CombinedHealth</div>
          <div className="text-[#dce8f5] text-xs">Policy Intelligence Platform</div>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <span className="bg-[#3b5f8a] text-[#dce8f5] text-xs px-2 py-1 rounded font-medium">UHC Commercial</span>
        </div>
      </header>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        <PolicySidebar onSelectPolicy={(q) => setPrefillQuery(q)} />
        <ChatWindow
          prefillQuery={prefillQuery}
          onPrefillConsumed={() => setPrefillQuery(null)}
        />
      </div>
    </div>
  );
}
