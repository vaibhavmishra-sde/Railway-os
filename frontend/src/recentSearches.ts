export type RecentSearch = {
  origin: string;
  destination: string;
  serviceDate: string;
  seatClass: string;
};

export const RECENT_SEARCHES_KEY = "railwayos.recent-searches";

export function addRecentSearch(search: RecentSearch, existing: RecentSearch[] = []): RecentSearch[] {
  const withoutDuplicate = existing.filter((item) => JSON.stringify(item) !== JSON.stringify(search));
  return [search, ...withoutDuplicate].slice(0, 5);
}

export function readRecentSearches(storage: Storage | null = typeof window === "undefined" ? null : window.localStorage): RecentSearch[] {
  if (!storage) return [];
  try {
    const value: unknown = JSON.parse(storage.getItem(RECENT_SEARCHES_KEY) ?? "[]");
    return Array.isArray(value) ? value.filter(isRecentSearch) : [];
  } catch { return []; }
}

function isRecentSearch(value: unknown): value is RecentSearch {
  if (!value || typeof value !== "object") return false;
  const item = value as Partial<RecentSearch>;
  return [item.origin, item.destination, item.serviceDate, item.seatClass].every((field) => typeof field === "string");
}

export function writeRecentSearches(searches: RecentSearch[], storage: Storage | null = typeof window === "undefined" ? null : window.localStorage) {
  storage?.setItem(RECENT_SEARCHES_KEY, JSON.stringify(searches));
}
