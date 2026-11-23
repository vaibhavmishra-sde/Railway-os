# Day 56 — Passenger discovery demo review

## Demo path

1. Start the API and frontend using the local setup instructions.
2. Register a synthetic passenger account when the registration endpoint is available.
3. Sign in with the passenger account and confirm the signed-in email appears in the header.
4. Search a route, select a station suggestion, choose a date/class, and submit the journey search.
5. Confirm loading, result, empty, and error states are understandable.

## Current review result

- Login → journey search is implemented in the frontend.
- Station autocomplete, recent-search persistence, result cards, and booking preview are available.
- The backend currently exposes login and `/auth/me`, but no registration route is registered in this checkout. Registration remains a documented follow-up rather than being faked in the demo.

## Verification

From `frontend/`:

```powershell
npm.cmd run build
npm.cmd run lint
```
