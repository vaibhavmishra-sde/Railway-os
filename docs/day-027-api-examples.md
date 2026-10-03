# Timetable API examples

List services for a date:

```http
GET /api/v1/services?service_date=2026-10-01&offset=0&limit=20
```

Retrieve a complete timetable:

```http
GET /api/v1/services/{service_id}
```

The detail response includes the service metadata and a `stops` array sorted
by `stop_sequence`.
