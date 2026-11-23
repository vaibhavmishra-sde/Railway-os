import { searchStatusMessage, searchStatusRole } from "./searchUi";

export function runSearchUiAssertions() {
  if (searchStatusMessage({ loading: true, error: null, resultCount: null, online: true }) !== "Searching available journeys…") throw new Error("Loading state is invalid");
  if (searchStatusMessage({ loading: false, error: "Request failed", resultCount: null, online: false }) !== "You appear to be offline. Check your connection and try again.") throw new Error("Offline state is invalid");
  if (searchStatusMessage({ loading: false, error: null, resultCount: 0, online: true }) !== "No journeys match these stations and travel preferences.") throw new Error("Empty state is invalid");
  if (searchStatusRole({ loading: false, error: "Request failed", resultCount: null, online: true }) !== "alert") throw new Error("Error state role is invalid");
}
