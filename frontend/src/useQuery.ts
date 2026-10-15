import { useCallback, useEffect, useState } from "react";

export type QueryState<T> = {
  data: T | null;
  error: Error | null;
  loading: boolean;
};

export function useQuery<T>(query: () => Promise<T>, dependencies: readonly unknown[] = []) {
  const [state, setState] = useState<QueryState<T>>({ data: null, error: null, loading: true });
  const run = useCallback(async () => {
    setState((current) => ({ ...current, loading: true, error: null }));
    try {
      setState({ data: await query(), error: null, loading: false });
    } catch (error) {
      setState({ data: null, error: error instanceof Error ? error : new Error("Request failed"), loading: false });
    }
  }, dependencies);
  useEffect(() => { void run(); }, [run]);
  return { ...state, refetch: run };
}
