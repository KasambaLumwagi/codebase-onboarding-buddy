const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const ingestRepo = async (repoUrl, apiKey = null) => {
  const response = await fetch(`${API_URL}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url: repoUrl, api_key: apiKey }),
  });
  if (!response.ok) {
    const err = await response.json();
    const detail = err.detail || "Ingestion failed";
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
  }
  return response.json();
};

export const sendMessage = async (sessionId, message) => {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Chat failed");
  }
  return response.json();
};

export const getSessions = async () => {
  const response = await fetch(`${API_URL}/sessions`);
  if (!response.ok) {
    throw new Error("Failed to fetch sessions");
  }
  return response.json();
};

export const getSessionMessages = async (sessionId) => {
  const response = await fetch(`${API_URL}/sessions/${sessionId}`);
  if (!response.ok) {
    throw new Error("Failed to load history");
  }
  return response.json();
};

export const deleteSession = async (sessionId) => {
  const response = await fetch(`${API_URL}/sessions/${sessionId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Failed to delete session");
  }
  return response.json();
};
