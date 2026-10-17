export const serviceStatusLabel = (status: string) => status.trim() || "Status unavailable";

export const serviceStatusTone = (status: string) => status.toLowerCase().includes("delay") || status.toLowerCase().includes("cancel") ? "warn" : "good";

export const serviceRouteLabel = (routeId: string) => routeId ? `Route ${routeId}` : "Route unavailable";

export const serviceDateLabel = (date: string) => date || "Date unavailable";

export const localDateInputValue = (date = new Date()) => {
  const offset = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 10);
};
