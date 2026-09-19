# RailwayOS — Entity Relationship Diagram

Generated as part of Day 015 (Month 1, Week 3).

```mermaid
erDiagram
    STATION {
        uuid id PK
        varchar code UK
        varchar name
        varchar city
        varchar state
        varchar timezone
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    TRAIN {
        uuid id PK
        varchar number UK
        varchar name
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    COACH {
        uuid id PK
        uuid train_id FK
        varchar coach_number
        varchar seat_class
        int total_seats
    }

    SEAT {
        uuid id PK
        uuid coach_id FK
        varchar seat_number
        varchar berth_type
    }

    ROUTE {
        uuid id PK
        varchar code UK
        varchar name
        float total_distance_km
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    ROUTE_STOP {
        uuid id PK
        uuid route_id FK
        uuid station_id FK
        int stop_sequence
        float distance_from_origin_km
    }

    TRAIN_SERVICE {
        uuid id PK
        uuid train_id FK
        uuid route_id FK
        date service_date
        varchar status
        timestamp created_at
        timestamp updated_at
    }

    SERVICE_STOP {
        uuid id PK
        uuid service_id FK
        uuid station_id FK
        int stop_sequence
        time scheduled_arrival
        time scheduled_departure
        varchar platform_number
    }

    TRAIN ||--o{ COACH : "has"
    COACH ||--o{ SEAT : "contains"
    ROUTE ||--o{ ROUTE_STOP : "ordered via"
    ROUTE_STOP }o--|| STATION : "at"
    TRAIN ||--o{ TRAIN_SERVICE : "runs as"
    ROUTE ||--o{ TRAIN_SERVICE : "follows"
    TRAIN_SERVICE ||--o{ SERVICE_STOP : "calls at"
    SERVICE_STOP }o--|| STATION : "at"
```

## Notes

- `COACH.seat_class` is an application-level enum stored as `VARCHAR`.
  Valid values: `FIRST_AC`, `SECOND_AC`, `THIRD_AC`, `SLEEPER`, `GENERAL`.
- `TRAIN_SERVICE.status` enum: `SCHEDULED`, `RUNNING`, `COMPLETED`, `CANCELLED`.
- `SEAT.berth_type` enum: `LOWER`, `MIDDLE`, `UPPER`, `SIDE_LOWER`, `SIDE_UPPER`, `SEAT`.
- Unique constraints:
  - `COACH(train_id, coach_number)`
  - `SEAT(coach_id, seat_number)`
  - `ROUTE_STOP(route_id, stop_sequence)` and `(route_id, station_id)`
  - `TRAIN_SERVICE(train_id, service_date)`
  - `SERVICE_STOP(service_id, stop_sequence)`
