# Day 44 — Direct journey search implementation

The Day 43 contract is now available at `GET /api/v1/search/journeys`.

The endpoint normalizes station codes, validates station existence, filters
dated services by ordered timetable stops, supports optional seat-class
availability, and returns deterministic departure/train/service ordering with
offset and limit pagination.

Examples:

```text
/api/v1/search/journeys?origin=ndls&destination=bct&service_date=2026-10-19
/api/v1/search/journeys?origin=NDLS&destination=BCT&service_date=2026-10-19&seat_class=THIRD_AC&limit=10
```

The response is intentionally limited to service, train, and selected stop
data. Schedule duration, fares, and inventory remain follow-up milestones.
