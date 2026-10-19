# Day 46 completion

Implemented schedule fields in `GET /api/v1/search/journeys`:

- `departure_time` and `arrival_time` use the boundary stop's available time.
- `duration_minutes` is calculated across midnight when necessary.
- `available_classes` is a deterministic, duplicate-free list from train
  coaches.

Coverage includes API response assertions and a direct overnight-duration
unit test.

Example result fragment:

```json
{
  "departure_time": "23:45:00",
  "arrival_time": "01:15:00",
  "duration_minutes": 90,
  "available_classes": ["SLEEPER", "THIRD_AC"]
}
```
