# RailwayOS Architecture Overview

> **Document Status**: Living document — updated as each phase is completed  
> **Last Updated**: Week 3 — Core Railway Schema (Days 15-21)

---

## System Architecture

RailwayOS follows a **Modular Monolith** architecture pattern.

### Why Modular Monolith?

| Concern | Modular Monolith | Microservices |
|---|---|---|
| Development speed (solo) | ✅ Fast | ❌ Slow (orchestration overhead) |
| Database transactions | ✅ Native ACID | ❌ Distributed sagas |
| Deployment complexity | ✅ Single deploy unit | ❌ Multiple services |
| Debugging | ✅ Single process trace | ❌ Distributed tracing required |
| Module boundaries | ✅ Enforced by code | ✅ Enforced by network |
| Future scalability | ✅ Extractable to services | ✅ Already services |

**Decision**: Modular Monolith for development phases. Individual modules designed for extraction if needed.

---

## Component Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                         RailwayOS System                       │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    React SPA (Vite)                     │   │
│  │                                                         │   │
│  │  Passenger UI  │  Operations Dashboard  │  Admin Panel  │   │
│  └──────────────────────────┬──────────────────────────────┘   │
│                             │ HTTP/REST + WebSocket            │
│  ┌──────────────────────────▼──────────────────────────────┐   │
│  │                  FastAPI Backend                         │   │
│  │                                                         │   │
│  │  auth  │  users  │  trains  │  stations  │  schedules  │   │
│  │  bookings  │  tickets  │  tracking  │  operations      │   │
│  │  notifications  │  analytics  │  ai  │  cargo          │   │
│  └──────────┬──────────────────────────────────────────────┘   │
│             │                                                  │
│    ┌────────┴──────────┐          ┌──────────────────────┐     │
│    │   PostgreSQL 15   │          │       Redis 7        │     │
│    │                   │          │                      │     │
│    │  Primary data     │          │  Cache (train search │     │
│    │  ACID transactions│          │  seat availability)  │     │
│    │  All modules      │          │  Pub/Sub (WebSocket  │     │
│    │                   │          │  broadcast)          │     │
│    └───────────────────┘          └──────────────────────┘     │
│                                                                │
│    ┌───────────────────────────────────────────────────────┐   │
│    │              ML Service (Python)                      │   │
│    │  Delay Prediction  │  Waitlist  │  Maintenance       │   │
│    └───────────────────────────────────────────────────────┘   │
│                                                                │
│    ┌───────────────────────────────────────────────────────┐   │
│    │           External: LLM API (AI Assistant)            │   │
│    │  Calls backend tools → never invents data             │   │
│    └───────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Examples

### Booking a Ticket
```
Passenger clicks "Book"
        ↓
React sends POST /api/v1/bookings
        ↓
FastAPI validates JWT + checks role = Passenger
        ↓
BookingService checks seat availability (PostgreSQL)
        ↓
BEGIN TRANSACTION
  ├── Lock seat row (SELECT FOR UPDATE)
  ├── Create booking record
  ├── Create ticket record
  ├── Generate PNR
  └── Update seat status
COMMIT (or ROLLBACK on any failure)
        ↓
Notification event queued
        ↓
Response: 201 Created with PNR
```

### Real-Time Train Location
```
Train sends location update (simulated)
        ↓
POST /api/v1/tracking/update (Operations role)
        ↓
Backend saves to train_locations table
        ↓
Redis Pub/Sub publishes event to channel "train:12345"
        ↓
WebSocket broadcaster receives message
        ↓
All subscribed clients receive location update
        ↓
React map updates in real-time
```

### AI Delay Prediction
```
Operations Manager requests prediction for Train 12345
        ↓
GET /api/v1/ai/delay-prediction/12345
        ↓
AI module loads trained model (scikit-learn)
        ↓
Fetches current features:
  - Previous delay history
  - Route congestion
  - Weather conditions (simulated)
  - Maintenance status
        ↓
Model predicts: 23 min delay, 78% confidence
        ↓
Explainability layer identifies top contributing factors
        ↓
Response includes prediction + explanation + data limitations disclaimer
```

---

## Security Layers

```
Internet
    ↓
[Rate Limiter]           ← Prevents API abuse
    ↓
[CORS Check]             ← Only allowed origins (frontend URL)
    ↓
[JWT Verification]       ← Is this a valid, non-expired token?
    ↓
[RBAC Check]             ← Does this role have permission for this endpoint?
    ↓
[Input Validation]       ← Pydantic schemas validate all request data
    ↓
[Business Logic]         ← Service layer processes the request
    ↓
[Audit Logging]          ← Sensitive operations recorded
    ↓
[Database]               ← SQLAlchemy parameterized queries (no SQL injection)
```

---

## Module Dependency Map

```
auth ←────────────── All modules (every module needs auth)
  │
users ←──────────── bookings, notifications, operations
  │
trains ←─────────── schedules, bookings, tracking, operations, cargo
  │
stations ←───────── routes, platforms, schedules, operations
  │
routes ←─────────── route_stations, schedules
  │
schedules ←──────── bookings, tracking, operations
  │
bookings ←───────── tickets, payments, notifications, waitlists
  │
tickets ←────────── pnr, notifications
  │
tracking ←───────── operations, notifications (WebSocket)
  │
ai ←─────────────── bookings (waitlist), operations (delay), maintenance
```

---

## Key Technical Decisions

| # | Decision | Rationale |
|---|---|---|
| 1 | Modular Monolith | Solo dev, shared transactions, extractable later |
| 2 | PostgreSQL | ACID for booking, relational integrity, indexing |
| 3 | FastAPI | Async, auto-docs, Pydantic, modern Python |
| 4 | JWT stateless auth | Frontend-agnostic, horizontally scalable |
| 5 | Redis pub/sub | WebSocket fan-out without DB polling |
| 6 | Tool-grounded AI | Prevents hallucination of railway data |
| 7 | Row-level locking | Prevents double booking under concurrency |

---

*This document is updated at the end of each phase.*

---

## Architecture Decision Records — Week 2 (Days 8-14)

| # | Decision | Context | Outcome |
|---|---|---|---|
| W2-1 | `pydantic-settings` for config | Need 12-factor env var loading without hard-coded secrets | `Settings` class reads `.env` and validates all required vars at startup |
| W2-2 | Single `API_PREFIX = /api/v1` | Future-proof versioning with minimal boilerplate | All routes registered under `/api/v1`; health endpoint available at both root and versioned path |
| W2-3 | Structured JSON logging | Ops need machine-parseable logs in production | `logging` module configured with ISO timestamp + severity; request-id propagated in error responses |
| W2-4 | Global `GlobalAPIException` handler | Inconsistent error shapes confuse API consumers | All unhandled application errors return `{error, request_id}` JSON with correct HTTP status |
| W2-5 | SQLAlchemy 2 with `pool_pre_ping` | Stale connections fail silently after idle periods | Engine pings before handing a connection to the app; session closed in `finally` block |
| W2-6 | Alembic for migrations | Manual SQL scripts are error-prone and hard to roll back | `alembic upgrade head` / `alembic downgrade -1` supported; script template committed |
| W2-7 | SQLite in-memory for unit tests | Spinning up PostgreSQL in every CI run is slow | `conftest.py` defaults to SQLite; `TEST_DATABASE_URL` overrides for integration tests |

---

## Data Model Layer — Week 3 (Days 15-21)

> **Last Updated**: Day 15 — ERD designed, model stubs committed

### ORM Module Layout

```
backend/app/models/
├── __init__.py     # Re-exports all models; imported by Alembic env.py
├── station.py      # Station
├── train.py        # Train, Coach, SeatClass
├── seat.py         # Seat, BerthType
├── route.py        # Route, RouteStop
└── service.py      # TrainService, ServiceStop, ServiceStatus
```

### Core Domain Model

The eight core entities fall into three conceptual groups:

**Physical assets**
- `Station` – a physical stop with a unique code (e.g. `NDLS`)
- `Train` – a trainset with a unique number (e.g. `12301`)
- `Coach` – a carriage on a train; carries `SeatClass`
- `Seat` – individual berth in a coach; carries `BerthType`

**Network topology**
- `Route` – ordered sequence of stations
- `RouteStop` – junction entity; holds sequence position and cumulative distance

**Scheduled operations**
- `TrainService` – a dated instance of a train on a route
- `ServiceStop` – scheduled arrival/departure at each call on a service

### Design Rationale

| Decision | Rationale |
|----------|-----------|
| Route separate from TrainService | One route can be served by many trains on many dates |
| RouteStop stores cumulative distance | Fare calculation avoids summing partial segments |
| ServiceStop times stored as `time` (no date) | Full datetime = `service_date` + `time`; avoids timezone ambiguity |
| SeatClass on Coach, not Seat | All seats in a coach share a class; simplifies availability queries |
| Python enums → PG VARCHAR/Enum | Validated in application layer; DB stores human-readable strings |
| UUID primary keys (string, length 36) | SQLite-compatible; no sequence dependency; safe for distributed seeds |

## Architecture Decision Records — Week 3 (Days 15-21)

| # | Decision | Context | Outcome |
|---|---|---|---|
| W3-1 | Models in `app/models/` package | Keeps ORM layer separate from API/core layers | All model files imported via `app.models.__init__` for Alembic auto-detect |
| W3-2 | UUID PKs stored as `String(36)` | SQLite does not have a native UUID type | Works in both SQLite tests and PostgreSQL production |
| W3-3 | `SeatClass` enum on Coach, not Seat | All berths in a coach share the same fare class | Availability queries need only aggregate by coach, not individual seat |
| W3-4 | `BerthType` on Seat | Berth position determines upper/lower preference for passengers | Enables seat-preference matching in Week 10 seat assignment |
| W3-5 | Nullable arrival/departure on ServiceStop | Origin has no arrival; terminus has no departure | Application layer enforces: exactly one of arrival/departure may be NULL |

