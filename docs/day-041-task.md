# Day 41 — Service search resilience

## Objective

Make dated service search resilient when passengers change dates quickly or
the API is temporarily unavailable.

## Scope

- Cancel obsolete service requests.
- Preserve a clear error state with a retry action.
- Validate service dates and classify warning statuses consistently.
- Document the verification path for the resilient service board.

## Verification

From `frontend/`, run `npm run build` and `npm run lint`. Change the selected
date twice quickly in a browser and confirm only the latest request populates
the board.
