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
