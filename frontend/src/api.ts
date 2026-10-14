const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export type Station = { id: string; code: string; name: string; city: string; state: string };
export type Service = { id: string; train_id: string; route_id: string; service_date: string; status: string };

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { headers: { "Content-Type": "application/json", ...options?.headers }, ...options });
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? `Request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export const api = {
  stations: (search: string) => request<Station[]>(`/stations?limit=8${search ? `&search=${encodeURIComponent(search)}` : ""}`),
  services: (date: string) => request<Service[]>(`/services?service_date=${encodeURIComponent(date)}`),
  login: (email: string, password: string) => request<{ access_token: string; expires_at: string }>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
};
