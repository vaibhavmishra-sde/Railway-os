const API_BASE = (import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1").replace(/\/$/, "");

export class ApiError extends Error {
  constructor(public readonly status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export type Station = { id: string; code: string; name: string; city: string; state: string };
export type Service = {
  id: string;
  train_id: string;
  route_id: string;
  service_date: string;
  status: "scheduled" | "boarding" | "departed" | "delayed" | "cancelled" | string;
};
export type LoginResponse = { access_token: string; expires_at: string };

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getAccessToken();
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { Accept: "application/json", "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options?.headers },
  });
  if (!response.ok) throw new ApiError(response.status, (await response.json().catch(() => null))?.detail ?? `Request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export const api = {
  stations: (search: string) => request<Station[]>(`/stations?limit=8${search ? `&search=${encodeURIComponent(search)}` : ""}`),
  services: (date: string, signal?: AbortSignal) => request<Service[]>(`/services?service_date=${encodeURIComponent(date)}`, { signal }),
  login: (email: string, password: string) => request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  me: () => request<{ id: string; email: string; is_active: boolean }>("/auth/me"),
};
import { getAccessToken } from "./auth";
