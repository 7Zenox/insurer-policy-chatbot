import { useEffect, useState } from "react";
import { fetchPolicies } from "../api/client";

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

  return (
    <aside className="policy-sidebar">
      <h2>Policies</h2>
      <input
        type="text"
        placeholder="Search policies..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <div className="filter-toggles">
        {["all", "medical", "drug"].map((f) => (
          <button key={f} className={filter === f ? "active" : ""} onClick={() => setFilter(f)}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>
      <ul>
        {filtered.map((p) => (
          <li key={p.name} onClick={() => onSelectPolicy(`Tell me about ${p.name}`)}>
            {p.name}
          </li>
        ))}
      </ul>
    </aside>
  );
}
