import { useCallback, useEffect, useState } from "react";

export type QueryState<T> = {
  data: T | null;
  error: Error | null;
  loading: boolean;
};

export function useQuery<T>(query: (signal: AbortSignal) => Promise<T>, dependencies: readonly unknown[] = []) {
  const [state, setState] = useState<QueryState<T>>({ data: null, error: null, loading: true });
  const run = useCallback(async (signal?: AbortSignal) => {
    setState((current) => ({ ...current, loading: true, error: null }));
    try {
      const data = await query(signal ?? new AbortController().signal);
      setState({ data, error: null, loading: false });
    } catch (error) {
      setState({ data: null, error: error instanceof Error ? error : new Error("Request failed"), loading: false });
    }
  }, dependencies);
  useEffect(() => {
    const controller = new AbortController();
    void run(controller.signal);
    return () => controller.abort();
  }, [run]);
  return { ...state, refetch: run };
}
