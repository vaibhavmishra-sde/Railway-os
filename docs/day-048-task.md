# Day 48 — Search pagination, sorting, and caching design

Journey search supports bounded pagination through `offset` and `limit`, plus
deterministic sorting with `sort=departure|duration|fare`. The optional
`descending=true` flag reverses the primary sort while retaining train number
and service id as tie-breakers.

## Cache design

The future read-through cache key is:

`journeys:{service_date}:{origin}:{destination}:{seat_class}:{sort}:{descending}:{offset}:{limit}`

Entries should use a short TTL because timetable and inventory data can change.
Writes to services, stops, routes, coaches, or seats should invalidate keys
for the affected service date and stations. The current implementation remains
database-backed and does not require Redis to run locally.

The response echoes `sort` and `descending` so clients can preserve the exact
ordering they requested while navigating pages. Descending mode reverses only
the selected primary field; train number and service id remain ascending
tie-breakers, which keeps adjacent pages stable.

The cache-key helper is canonical: station codes are trimmed and uppercased,
and every filter and pagination value is included. It is intentionally kept
separate from the database-backed endpoint until a Redis read-through layer is
introduced.
