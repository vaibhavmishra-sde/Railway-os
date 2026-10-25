# Day 49 — Journey planner integration

## Goal

Connect the passenger journey planner to the existing journey-search API.

## Acceptance criteria

- Departure and arrival fields are controlled inputs.
- A search sends normalized station values and the selected service date.
- Empty station input is reported inline without making a request.
- Successful searches report the result count and route.
- Search failures remain visible to assistive technology.

## Verification

Run `npm.cmd run build` from `frontend/` and manually verify a search with
station suggestions and a no-results response.
