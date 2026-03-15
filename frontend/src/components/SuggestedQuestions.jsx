import { MessageSquare, Search, FileText, Dna } from "lucide-react";

const QUESTIONS = [
  { icon: MessageSquare, text: "Is bariatric surgery covered for BMI > 35?" },
  { icon: Search, text: "What are the prior auth requirements for MRI?" },
  { icon: FileText, text: "What does CPT code 64493 cover?" },
  { icon: Dna, text: "When is genetic testing covered?" },
];

export default function SuggestedQuestions({ onSelect }) {
  return (
    <div className="flex flex-col items-center justify-center flex-1 py-12 px-4">
      <div className="w-12 h-12 bg-[#dce8f5] rounded-full flex items-center justify-center mb-4">
        <MessageSquare size={22} className="text-[#3b5f8a]" />
      </div>
      <h2 className="text-[#1a2e4a] font-semibold text-lg mb-1">Policy Assistant</h2>
      <p className="text-[#6b7280] text-sm mb-8 text-center max-w-sm">
        Ask questions about UHC commercial medical and drug policies. Get instant answers with source citations.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full max-w-xl">
        {QUESTIONS.map(({ icon: Icon, text }) => (
          <button
            key={text}
            onClick={() => onSelect(text)}
            className="flex items-start gap-3 text-left px-4 py-3 bg-white border border-[#e5e7eb] rounded-lg hover:border-[#3b5f8a] hover:bg-[#f0f6ff] transition-colors text-sm text-[#111827]"
          >
            <Icon size={15} className="text-[#3b5f8a] shrink-0 mt-0.5" />
            <span>{text}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
