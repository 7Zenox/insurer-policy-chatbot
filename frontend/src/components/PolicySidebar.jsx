import { useEffect, useState } from "react";
import { fetchPolicies } from "../api/client";
import { Search, FileText, Pill, LayoutList } from "lucide-react";

export default function PolicySidebar({ onSelectPolicy }) {
  const [policies, setPolicies] = useState([]);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchPolicies().then((data) => setPolicies(data.policies || []));
  }, []);

  const filtered = policies.filter((p) => {
    const matchesSearch = p.name.toLowerCase().includes(search.toLowerCase());
    const matchesFilter =
      filter === "all" ||
      (filter === "drug" && p.name.toLowerCase().includes("drug")) ||
      (filter === "medical" && !p.name.toLowerCase().includes("drug"));
    return matchesSearch && matchesFilter;
  });

  const filters = [
    { key: "all", label: "All", icon: LayoutList },
    { key: "medical", label: "Medical", icon: FileText },
    { key: "drug", label: "Drug", icon: Pill },
  ];

  return (
    <aside className="w-72 bg-white border-r border-[#e5e7eb] flex flex-col shrink-0">
      {/* Sidebar header */}
      <div className="px-4 pt-4 pb-3 border-b border-[#e5e7eb]">
        <div className="text-[#1a2e4a] font-semibold text-sm mb-3">Policy Library</div>
        {/* Search */}
        <div className="relative">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9ca3af]" />
          <input
            type="text"
            placeholder="Search policies..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-8 pr-3 py-2 text-sm border border-[#e5e7eb] rounded-lg bg-[#f9fafb] text-[#111827] placeholder-[#9ca3af] focus:outline-none focus:border-[#3b5f8a] focus:ring-1 focus:ring-[#3b5f8a]"
          />
        </div>
        {/* Filter tabs */}
        <div className="flex gap-1 mt-2">
          {filters.map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setFilter(key)}
              className={`flex items-center gap-1.5 flex-1 justify-center px-2 py-1.5 rounded text-xs font-medium transition-colors
                ${filter === key
                  ? "bg-[#1a2e4a] text-white"
                  : "text-[#6b7280] hover:bg-[#f3f4f6]"
                }`}
            >
              <Icon size={12} />
              {label}
            </button>
          ))}
        </div>
        <div className="text-[#9ca3af] text-xs mt-2">{filtered.length} policies</div>
      </div>

      {/* Policy list */}
      <div className="flex-1 overflow-y-auto py-1">
        {filtered.map((p) => (
          <button
            key={p.name}
            onClick={() => onSelectPolicy(`Tell me about ${p.name}`)}
            className="w-full text-left px-4 py-2.5 hover:bg-[#f3f4f6] transition-colors group"
          >
            <div className="flex items-start gap-2">
              <FileText size={13} className="text-[#9ca3af] group-hover:text-[#3b5f8a] shrink-0 mt-0.5 transition-colors" />
              <div>
                <div className="text-[#111827] text-xs font-medium leading-snug">{p.name}</div>
                {p.effective_date && (
                  <div className="text-[#9ca3af] text-[10px] mt-0.5">{p.effective_date}</div>
                )}
              </div>
            </div>
          </button>
        ))}
      </div>
    </aside>
  );
}
