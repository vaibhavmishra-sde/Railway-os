# Day 43 — Direct journey search contract

## Objective

Define the stable request and response contract for searching direct dated
train journeys. Implementation is intentionally split into the following days:
station validation, ordered-stop matching, schedule calculation, fares, and
pagination/caching.

## Contract

`GET /api/v1/search/journeys`

Required query parameters:

- `origin`: station code, case-insensitive.
- `destination`: station code, case-insensitive.
- `service_date`: ISO-8601 calendar date.

Optional parameters:

- `seat_class`: requested `SeatClass` value.
- `offset`: non-negative result offset; defaults to `0`.
- `limit`: page size from `1` through `100`; defaults to `50`.

The response is an envelope containing normalized query values, `total`,
pagination metadata, and `items`. Each item identifies the dated service,
train, and the matching origin/destination timetable stops. A service is a
direct match only when both stations occur in its ordered stop list and the
origin sequence is lower than the destination sequence.

## Rules

- Station codes are normalized to uppercase for matching and response values.
- Identical origin and destination codes are rejected with HTTP 422.
- Unknown stations are rejected with HTTP 404.
- A valid search with no matching service returns HTTP 200 and `items: []`.
- Search results have deterministic ordering by departure time, then train
  number, then service id.

The Pydantic models in `backend/app/api/v1/schemas.py` are the source of truth
for the generated OpenAPI schema. Schedule duration, fare, and availability
fields will be added only when their backend rules are implemented.
