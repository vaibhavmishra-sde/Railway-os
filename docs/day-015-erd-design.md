# Day 015 — ERD Design Notes: Core Railway Schema

**Date:** 2026-09-20  
**Plan reference:** Month 1, Week 3, Day 15

## Goal

Design the Entity-Relationship Diagram (ERD) for the seven core entities that
form the backbone of RailwayOS:

1. **Station** – a physical stop on a rail network
2. **Train** – a physical trainset with a unique number
3. **Coach** – a carriage attached to a train with a class designation
4. **Seat** – an individual seat position within a coach
5. **Route** – a named path made up of ordered station stops
6. **RouteStop** – a junction entity binding a station to a route with sequence and distance
7. **TrainService** – a dated instance of a train running a route
8. **ServiceStop** – scheduled arrival/departure time for each stop on a service

## Design decisions

| Decision | Rationale |
|----------|-----------|
| Route is separate from TrainService | Multiple services can share the same route on different days |
| RouteStop stores cumulative distance | Enables fare calculation without summing partial distances |
| ServiceStop times stored as `time` (no date) | Combined with TrainService.service_date to get a full datetime |
| Seat class is on Coach, not Seat | All seats in a coach share the same class (AC 1, AC 2, Sleeper, etc.) |
| SeatClass is a Python enum → PG VARCHAR | Keeps the DB simple; enum validated in application layer |
| Soft-delete not required at this stage | Week 12 cancellations use a status flag, not row deletion |

## Entities and attributes

### Station
- `id` (PK, UUID)
- `code` (UNIQUE, 3-5 chars, e.g. "NDLS")
- `name` (full station name)
- `city`
- `state`
- `timezone` (IANA tz string)
- `is_active` (bool, default True)
- `created_at`, `updated_at`

### Train
- `id` (PK, UUID)
- `number` (UNIQUE, e.g. "12301")
- `name` (e.g. "Rajdhani Express")
- `is_active`
- `created_at`, `updated_at`

### Coach
- `id` (PK, UUID)
- `train_id` (FK → Train)
- `coach_number` (e.g. "B1", "A2")
- `seat_class` (enum: FIRST_AC, SECOND_AC, THIRD_AC, SLEEPER, GENERAL)
- `total_seats`
- UNIQUE (`train_id`, `coach_number`)

### Seat
- `id` (PK, UUID)
- `coach_id` (FK → Coach)
- `seat_number` (e.g. "1", "32")
- `berth_type` (LOWER, MIDDLE, UPPER, SIDE_LOWER, SIDE_UPPER, SEAT)
- UNIQUE (`coach_id`, `seat_number`)

### Route
- `id` (PK, UUID)
- `code` (UNIQUE, e.g. "DEL-MUM")
- `name`
- `total_distance_km`
- `is_active`
- `created_at`, `updated_at`

### RouteStop
- `id` (PK, UUID)
- `route_id` (FK → Route)
- `station_id` (FK → Station)
- `stop_sequence` (int, 1-based)
- `distance_from_origin_km` (float)
- UNIQUE (`route_id`, `stop_sequence`)
- UNIQUE (`route_id`, `station_id`)

### TrainService
- `id` (PK, UUID)
- `train_id` (FK → Train)
- `route_id` (FK → Route)
- `service_date` (date)
- `status` (enum: SCHEDULED, RUNNING, COMPLETED, CANCELLED)
- `created_at`, `updated_at`
- UNIQUE (`train_id`, `service_date`)

### ServiceStop
- `id` (PK, UUID)
- `service_id` (FK → TrainService)
- `station_id` (FK → Station)
- `stop_sequence`
- `scheduled_arrival` (time, nullable for origin)
- `scheduled_departure` (time, nullable for terminus)
- `platform_number` (varchar, nullable)
- UNIQUE (`service_id`, `stop_sequence`)

## Relationships summary

```
Train ──< Coach ──< Seat
Route ──< RouteStop >── Station
Train + Route ──> TrainService ──< ServiceStop >── Station
```
