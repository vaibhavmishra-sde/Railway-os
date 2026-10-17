export const serviceStatusClass = (status: string) => status === "On time" ? "good" : "warn";

export const serviceStatusLabel = (status: string) => status.trim() || "Status unavailable";

export const serviceDateLabel = (date: string) => date || "Date unavailable";

export const serviceRouteLabel = (routeId: string) => routeId ? `Route ${routeId}` : "Route unavailable";

export function runServiceBoardAssertions() {
  if (serviceStatusClass("On time") !== "good" || serviceStatusClass("Delayed 12m") !== "warn" || serviceStatusLabel("") !== "Status unavailable" || serviceDateLabel("") !== "Date unavailable" || serviceRouteLabel("") !== "Route unavailable") {
    throw new Error("Service status mapping is invalid");
  }
}
