export type SearchUiState = {
  loading: boolean;
  error: string | null;
  resultCount: number | null;
  online: boolean;
};

export function searchStatusMessage(state: SearchUiState): string | null {
  if (state.loading) return "Searching available journeys…";
  if (state.error) return state.online ? state.error : "You appear to be offline. Check your connection and try again.";
  if (state.resultCount === 0) return "No journeys match these stations and travel preferences.";
  if (state.resultCount !== null) return `${state.resultCount} journey${state.resultCount === 1 ? "" : "s"} found.`;
  return null;
}

export const searchStatusRole = (state: SearchUiState) => state.error ? "alert" : "status";
