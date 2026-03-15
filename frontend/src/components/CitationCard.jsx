import { useState } from "react";

export default function CitationCard({ citation }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="citation-card" onClick={() => setExpanded(!expanded)}>
      <div className="citation-header">
        <span>📄 {citation.policy_name}</span>
        {citation.section && <span className="section-tag">{citation.section.replace(/_/g, " ")}</span>}
      </div>
      {citation.effective_date && <div className="citation-meta">Effective: {citation.effective_date}</div>}
      {citation.url && (
        <a href={citation.url} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}>
          View original PDF ↗
        </a>
      )}
      {expanded && citation.excerpt && <div className="citation-excerpt">{citation.excerpt}</div>}
    </div>
  );
}
