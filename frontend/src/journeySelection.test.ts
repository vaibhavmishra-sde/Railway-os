import { journeyRouteLabel, journeySelectionLabel } from "./journeySelection";

export function runJourneySelectionAssertions() {
  if (journeySelectionLabel(null) !== "No journey selected" || journeyRouteLabel("NDLS", "BCT") !== "NDLS → BCT") {
    throw new Error("Journey selection mapping is invalid");
  }
}
