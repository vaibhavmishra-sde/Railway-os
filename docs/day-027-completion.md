# Day 27 completion

Day 27 delivers the read-oriented timetable surface for dated train services.

## Endpoints

- `GET /api/v1/services?service_date=YYYY-MM-DD` lists services for a date.
- `GET /api/v1/services/{service_id}` returns a service and its ordered stops.
- `GET /api/v1/services/{service_id}/stops` returns only the stop collection.

Service lists support zero-based `offset` pagination. `limit` defaults to 50
and is capped at 100. Invalid pagination values return HTTP 422. A service
cannot contain two stops with the same sequence number; duplicate positions
return HTTP 409.
