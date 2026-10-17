export const serviceStatusLabel = (status: string) => status.trim() || "Status unavailable";

export const serviceRouteLabel = (routeId: string) => routeId ? `Route ${routeId}` : "Route unavailable";

export const serviceDateLabel = (date: string) => date || "Date unavailable";
