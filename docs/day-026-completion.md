# Day 26 completion

Day 26 delivers the first read-oriented discovery surface for trains and
routes. Consumers can list or retrieve active trains and routes, and inspect
their coaches or ordered stops.

List endpoints support a small, predictable query contract:

- `search` matches the public number/code or name.
- `offset` is zero-based and cannot be negative.
- `limit` defaults to 50 and is capped at 100.

The API intentionally returns active records only. Missing or inactive detail
records return HTTP 404, keeping public discovery consistent with station APIs.
