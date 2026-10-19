# Day 46 completion

Implemented schedule fields in `GET /api/v1/search/journeys`:

- `departure_time` and `arrival_time` use the boundary stop's available time.
- `duration_minutes` is calculated across midnight when necessary.
- `available_classes` is a deterministic, duplicate-free list from train
  coaches.

Coverage includes API response assertions and a direct overnight-duration
unit test.
