import type { JourneySearchItem } from "./api";

export const journeySelectionLabel = (journey: JourneySearchItem | null) => {
  if (!journey) return "No journey selected";
  return `${journey.train_name} · ${journey.train_number}`;
};

export const journeyRouteLabel = (origin: string, destination: string) =>
  `${origin || "Origin unavailable"} → ${destination || "Destination unavailable"}`;
