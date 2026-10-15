# Day 39 — Frontend API and query foundation

The frontend now has a typed `ApiError` with an HTTP status, a reusable
`useQuery` state helper, and an ESLint 10 flat configuration. Service data can
be loaded independently of the journey search form and exposes loading and
error states to the UI.

## Verification

From `frontend/`:

```sh
npm run build
npm run lint
```
