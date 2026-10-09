import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

const api = axios.create({ baseURL: API_BASE_URL, timeout: 8000 });

export async function getDashboard() {
  const response = await api.get("/dashboard");
  return response.data;
}

export async function getHistory(limit = 35) {
  const response = await api.get(`/history?limit=${limit}`);
  return response.data.history;
}

export async function getEvents(limit = 20) {
  const response = await api.get(`/events?limit=${limit}`);
  return response.data.events;
}

export async function simulateHighLoad() {
  const response = await api.post("/simulation/high-load");
  return response.data;
}

export async function restoreNormal() {
  const response = await api.post("/simulation/normal");
  return response.data;
}
