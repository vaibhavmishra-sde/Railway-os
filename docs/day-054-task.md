# Day 54 — Search resilience states

## Objective

Make journey search and live services communicate loading, empty, offline, and API failure states clearly.

## Done

- Kept the search submit control visibly busy while a request is in flight.
- Preserved explicit journey and live-service API errors for users.
- Added an offline-specific search error message when the browser has no connection.
- Made zero-result searches read as “No journeys” instead of a misleading count.

## Verification

From `frontend/`:

```sh
npm.cmd run build
npm.cmd run lint
```
