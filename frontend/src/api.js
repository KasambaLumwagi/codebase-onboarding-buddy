const API_URL = "http://localhost:8000";

export const ingestRepo = async (repoUrl, apiKey) => {
  const response = await fetch(`${API_URL}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url: repoUrl, api_key: apiKey }),
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Ingestion failed");
  }
  return response.json();
};

export const sendMessage = async (message) => {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Chat failed");
  }
  return response.json();
};
