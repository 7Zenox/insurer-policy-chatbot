import { useState } from "react";
import { FileText, ChevronDown, ChevronUp, ExternalLink } from "lucide-react";

export default function CitationCard({ citation }) {
  const [expanded, setExpanded] = useState(false);

  const sectionLabel = citation.section
    ? citation.section.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())
    : null;

  return (
    <div className="bg-[#f8fafc] border border-[#e5e7eb] rounded-lg overflow-hidden text-xs">
      <div
        className="flex items-start gap-2 px-3 py-2 cursor-pointer hover:bg-[#dce8f5] transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <FileText size={13} className="text-[#3b5f8a] shrink-0 mt-0.5" />
        <div className="flex-1 min-w-0">
          <div className="font-medium text-[#1a2e4a] truncate">{citation.policy_name}</div>
          <div className="flex items-center gap-2 mt-0.5 flex-wrap">
            {sectionLabel && (
              <span className="bg-[#dce8f5] text-[#3b5f8a] px-1.5 py-0.5 rounded text-[10px] font-medium">
                {sectionLabel}
              </span>
            )}
            {citation.effective_date && (
              <span className="text-[#6b7280]">Effective {citation.effective_date}</span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-1 shrink-0">
          {citation.url && (
            <a
              href={citation.url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="text-[#3b5f8a] hover:text-[#1a2e4a] transition-colors"
            >
              <ExternalLink size={12} />
            </a>
          )}
          {expanded ? <ChevronUp size={12} className="text-[#6b7280]" /> : <ChevronDown size={12} className="text-[#6b7280]" />}
        </div>
      </div>
      {expanded && citation.excerpt && (
        <div className="px-3 py-2 border-t border-[#e5e7eb] text-[#6b7280] leading-relaxed bg-white">
          {citation.excerpt}
        </div>
      )}
    </div>
  );
}
