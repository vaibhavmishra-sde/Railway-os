# Day 42 — Frontend accessibility and auth review

## Objective

Make the authenticated dashboard shell ready for a mobile demo and verify the
frontend auth integration.

## Delivered

- Login calls the API, stores the short-lived access token in `sessionStorage`,
  and verifies the session through `/auth/me`.
- Authenticated API requests automatically include a bearer token.
- Sign out clears the local session and returns the header to its signed-out
  state.
- Login and booking dialogs have accessible labels, required fields, and
  visible keyboard focus states.
- Service cards collapse into a readable mobile layout below 520px.
- Reduced-motion preferences are respected.

## Verification

From `frontend/`:

```bash
npm run build
npm run lint
```

Manual path: open the dashboard, choose **Sign in**, submit valid credentials,
confirm the account control changes to **Sign out**, resize to a narrow viewport,
and confirm service cards remain readable. Sign out should remove the token from
the session.
