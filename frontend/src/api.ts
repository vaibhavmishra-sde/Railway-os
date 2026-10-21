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
export type JourneySort = "departure" | "duration" | "fare";
export type JourneySearchParams = {
  origin: string;
  destination: string;
  serviceDate: string;
  seatClass?: string;
  offset?: number;
  limit?: number;
  sort?: JourneySort;
  descending?: boolean;
};
export type JourneySearchItem = {
  service_id: number;
  train_number: string;
  train_name: string;
  service_date: string;
  departure_time: string | null;
  arrival_time: string | null;
  duration_minutes: number | null;
  available_classes: string[];
  fares: Record<string, number>;
};
export type JourneySearchResponse = {
  items: JourneySearchItem[];
  origin: string;
  destination: string;
  service_date: string;
  total: number;
  offset: number;
  limit: number;
  sort: JourneySort;
  descending: boolean;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getAccessToken();
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { Accept: "application/json", "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options?.headers },
  });
  if (!response.ok) throw new ApiError(response.status, (await response.json().catch(() => null))?.detail ?? `Request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export function journeySearchPath(params: JourneySearchParams): string {
  const query = new URLSearchParams({
    origin: params.origin.trim().toUpperCase(),
    destination: params.destination.trim().toUpperCase(),
    service_date: params.serviceDate,
    offset: String(params.offset ?? 0),
    limit: String(params.limit ?? 50),
    sort: params.sort ?? "departure",
    descending: String(params.descending ?? false),
  });
  if (params.seatClass) query.set("seat_class", params.seatClass);
  return `/search/journeys?${query}`;
}

export const api = {
  stations: (search: string) => request<Station[]>(`/stations?limit=8${search ? `&search=${encodeURIComponent(search)}` : ""}`),
  services: (date: string, signal?: AbortSignal) => request<Service[]>(`/services?service_date=${encodeURIComponent(date)}`, { signal }),
  journeys: (params: JourneySearchParams, signal?: AbortSignal) => request<JourneySearchResponse>(journeySearchPath(params), { signal }),
  login: (email: string, password: string) => request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  me: () => request<{ id: string; email: string; is_active: boolean }>("/auth/me"),
};
import { getAccessToken } from "./auth";
