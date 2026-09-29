# Timetable API usage

The seeded timetable is available through the public read-only service API:

```text
GET /api/v1/services?service_date=2026-10-01
GET /api/v1/services/{service_id}/stops
```

Services are returned in train order and stops are returned by their sequence
along the route. The API exposes synthetic data only.
