# Day 57 — Booking ERD

RailwayOS uses a booking aggregate to keep the passenger, selected service,
travellers, allocated seats, fare snapshot, simulated payment attempts, and
audit history connected without duplicating timetable data.

```mermaid
erDiagram
    USER ||--o{ BOOKING : places
    TRAIN_SERVICE ||--o{ BOOKING : receives
    BOOKING ||--|{ TRAVELLER : includes
    BOOKING ||--o{ TICKET : issues
    BOOKING ||--o{ PAYMENT_ATTEMPT : records
    BOOKING ||--o{ BOOKING_EVENT : records
    TICKET }o--|| SEAT : allocates
    TICKET }o--|| STATION : boards_at
    TICKET }o--|| STATION : exits_at

    BOOKING {
        uuid id PK
        varchar pnr UK
        uuid user_id FK
        uuid service_id FK
        varchar status
        varchar currency
        int total_amount_minor
        varchar idempotency_key UK
        timestamp expires_at
        timestamp created_at
        timestamp updated_at
    }

    TRAVELLER {
        uuid id PK
        uuid booking_id FK
        varchar full_name
        date date_of_birth
        varchar identity_reference
    }

    TICKET {
        uuid id PK
        uuid booking_id FK
        uuid traveller_id FK
        uuid seat_id FK
        uuid boarding_station_id FK
        uuid arrival_station_id FK
        varchar status
        int fare_amount_minor
    }

    PAYMENT_ATTEMPT {
        uuid id PK
        uuid booking_id FK
        varchar provider
        varchar status
        int amount_minor
        varchar provider_reference
        timestamp created_at
    }

    BOOKING_EVENT {
        uuid id PK
        uuid booking_id FK
        varchar from_status
        varchar to_status
        varchar reason
        varchar actor_type
        timestamp created_at
    }
```

Existing `USER`, `TRAIN_SERVICE`, `SEAT`, and `STATION` records remain the
source of identity, timetable, inventory, and network truth. Booking records
store immutable fare and route snapshots so later timetable changes do not
rewrite a purchased ticket.
