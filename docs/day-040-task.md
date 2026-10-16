# Day 40 — Dated service search

## Objective

Connect the passenger service board to the dated-services API so the selected
travel date is reflected in the request and in the displayed results.

## Done

- Removed static service fixtures from the board.
- Added a date-driven request to `GET /api/v1/services`.
- Added loading, empty, and API error states.
- Preserved station autocomplete while the service query refreshes.

## Verification

From `frontend/`:

```sh
npm run build
npm run lint
```
