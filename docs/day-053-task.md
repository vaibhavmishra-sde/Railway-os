# Day 53 — Selected journey preview

## Objective

Carry the passenger's selected search result into the booking preview so the next step is unambiguous.

## Done

- Stored the selected journey when a result card is selected.
- Displayed train identity, route, service date, and timing in the booking preview.
- Added small pure helpers and assertions for selection and route labels.

## Verification

From `frontend/`:

```sh
npm.cmd run build
npm.cmd run lint
```

Build passed. Lint passed with one existing Fast Refresh warning in `main.tsx`.
