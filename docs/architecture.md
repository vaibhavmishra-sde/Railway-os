# RailwayOS Architecture Overview

> **Document Status**: Living document — updated as each phase is completed  
> **Last Updated**: Phase 1

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
