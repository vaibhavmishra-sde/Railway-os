# Day 52 — Journey result cards

## Objective

Present direct journey-search responses as useful, scannable result cards.

## Done

- Added result cards for train identity, number, and service date.
- Added departure/arrival timing and computed duration.
- Added available coach classes and deterministic INR fare breakdown.
- Added a clear select action that opens the existing booking preview.
- Kept unavailable timing, class, and fare data explicit instead of guessing.

## Verification

From `frontend/`:

```sh
npm.cmd run build
npm.cmd run lint
```
