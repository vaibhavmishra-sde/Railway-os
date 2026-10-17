export const serviceStatusClass = (status: string) => status === "On time" ? "good" : "warn";

export const serviceStatusLabel = (status: string) => status.trim() || "Status unavailable";

export const serviceDateLabel = (date: string) => date || "Date unavailable";

export const serviceRouteLabel = (routeId: string) => routeId ? `Route ${routeId}` : "Route unavailable";

export const isServiceDate = (value: string) => /^\d{4}-\d{2}-\d{2}$/.test(value);
export const serviceStatusTone = (status: string) => status.toLowerCase().includes("delay") || status.toLowerCase().includes("cancel") ? "warn" : "good";

export function runServiceBoardAssertions() {
  if (serviceStatusClass("On time") !== "good" || serviceStatusClass("Delayed 12m") !== "warn" || serviceStatusLabel("") !== "Status unavailable" || serviceDateLabel("") !== "Date unavailable" || serviceRouteLabel("") !== "Route unavailable" || !isServiceDate("2026-10-17") || isServiceDate("17-10-2026") || serviceStatusTone("Delayed") !== "warn") {
    throw new Error("Service status mapping is invalid");
  }
}
