# Frontend journey search

The frontend API client exposes `api.journeys` for the dated direct-journey
endpoint. `journeySearchPath` normalizes station codes and preserves the
server contract for `offset`, `limit`, `sort`, `descending`, and `seat_class`.

The response keeps the server's `total`, page metadata, and fare map so a
results screen can render pagination without duplicating search rules.
