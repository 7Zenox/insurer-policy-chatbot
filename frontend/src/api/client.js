const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchPolicies(provider = "uhc") {
  const res = await fetch(`${BASE_URL}/policies?provider=${provider}`);
  return res.json();
}

export { BASE_URL };
