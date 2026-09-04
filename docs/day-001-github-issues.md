# Day 001 — GitHub Issues & Milestones for Months 1-4

This file contains every milestone and issue to paste into GitHub once your
repository is created.  Create milestones first, then issues.

---

## Step 1 — Create 4 Milestones

Go to **GitHub → your repo → Issues → Milestones → New milestone** and add:

| Title | Description | Due date |
|---|---|---|
| Month 1: Foundation & Railway Data | Platform, dev environment, core schema, seed data, public APIs | (optional) |
| Month 2: Auth, Search & Passenger Portal | Identity, JWT, journey search backend + frontend | (optional) |
| Month 3: Booking, PNR & Inventory | Safe booking, cancellation, RAC/waitlist, inventory integrity | (optional) |
| Month 4: Operations & Live Status | Ops dashboard, real-time WebSocket, Docker, v1.0.0 release | (optional) |

---

## Step 2 — Create Labels

Create these labels in **GitHub → Issues → Labels → New label**:

| Label | Color | Description |
|---|---|---|
| `setup` | `#e4e669` | Initial project setup |
| `infrastructure` | `#0075ca` | Docker, CI, deployment |
| `backend` | `#6f42c1` | FastAPI / Python work |
| `frontend` | `#fd8d3c` | React / Vite work |
| `database` | `#1d76db` | Models, migrations, seeds |
| `api` | `#7057ff` | REST API endpoints |
| `auth` | `#e11d48` | Authentication & authorization |
| `search` | `#0e8a16` | Journey search feature |
| `booking` | `#b60205` | Booking / PNR / tickets |
| `operations` | `#d93f0b` | Operations dashboard |
| `realtime` | `#0052cc` | WebSocket / live updates |
| `testing` | `#bfd4f2` | Tests and coverage |
| `data` | `#c2e0c6` | Seed data & datasets |
| `docs` | `#f9d0c4` | Documentation |
| `design` | `#fef2c0` | Design decisions & ERDs |
| `ci` | `#ededed` | GitHub Actions / CI |
| `devops` | `#e4e669` | Docker, Compose, deploy |
| `review` | `#d4c5f9` | Weekly review tasks |
| `a11y` | `#0075ca` | Accessibility |
| `release` | `#b60205` | Release milestones |

---

## Step 3 — Create Issues

### Milestone: Month 1 — Foundation & Railway Data

#### Week 1: Development Foundation

| Day | Title | Labels | Done when |
|---|---|---|---|
| 1 | Read roadmap; create GitHub issues/milestones; verify prerequisites | `setup` | Issue board has four monthly milestones |
| 2 | Copy `.env.example` → `.env`; set dev passwords; validate Docker config | `setup` | `docker compose config` succeeds; `.env` git-ignored |
| 3 | Start PostgreSQL + Redis via Docker; check health, ports, volumes | `infrastructure` | Both containers report healthy |
| 4 | Create backend Python venv and dependency manifest | `backend`, `setup` | Clean venv installs all backend deps |
| 5 | Create FastAPI application package and `GET /health` | `backend`, `api` | API starts; health returns HTTP 200 |
| 6 | Add pytest, health test, formatter, linter, pre-commit | `backend`, `testing` | Test, format, lint commands pass |
| 7 | Add GitHub Actions backend checks workflow; write setup instructions | `ci` | Push/PR CI runs basic checks |

#### Week 2: Backend Architecture

| Day | Title | Labels | Done when |
|---|---|---|---|
| 8 | App settings with `pydantic-settings` and env validation | `backend` | App reads config without hard-coded secrets |
| 9 | API prefix/versioning, router structure, OpenAPI metadata | `backend`, `api` | Swagger groups under `/api/v1` |
| 10 | Request IDs, structured logging, global error response format | `backend` | Invalid request returns consistent JSON error |
| 11 | SQLAlchemy engine/session and DB connectivity check | `backend`, `database` | Backend connects to PostgreSQL |
| 12 | Initialize Alembic; blank migration workflow | `backend`, `database` | `alembic upgrade head` runs successfully |
| 13 | DB test fixture strategy; separate test database config | `backend`, `testing` | Tests don't touch dev data |
| 14 | Week 2 review: refactor imports, architecture docs, full checks | `review` | Fresh backend setup and checks pass |

#### Week 3: Core Railway Schema

| Day | Title | Labels | Done when |
|---|---|---|---|
| 15 | Design ERD: stations, trains, routes, services, stops, coaches, seats | `database`, `design` | ERD committed in `docs/` |
| 16 | Station model, migration, schemas, validation | `database`, `backend` | Station table migrates; tests pass |
| 17 | Train and Coach models with train-number constraints | `database`, `backend` | Train/coaches migrate with valid relations |
| 18 | Route and RouteStop models with ordered stops and distances | `database`, `backend` | Stop order enforced by constraints |
| 19 | TrainService and ServiceStop models for dated timetable | `database`, `backend` | A service can represent a train on a specific date |
| 20 | Seat model, seat class, coach-seat uniqueness | `database`, `backend` | No coach contains duplicate seat numbers |
| 21 | Model and migration tests; schema reference document | `database`, `testing` | All core-model tests pass |

#### Week 4: Seed Data & Public APIs

| Day | Title | Labels | Done when |
|---|---|---|---|
| 22 | Define synthetic network: 10-20 stations, 5-10 services | `data`, `design` | Dataset assumptions documented |
| 23 | Idempotent seed command for stations and routes | `data`, `backend` | Re-running creates no duplicates |
| 24 | Extend seeds: trains, coaches, seats, services, stop times | `data`, `backend` | Fresh DB contains usable timetable |
| 25 | Station list/detail APIs with search and pagination | `api`, `backend` | Tests cover list, search, missing station |
| 26 | Train and route detail APIs | `api`, `backend` | Route response contains ordered stops |
| 27 | Timetable/service detail APIs | `api`, `backend` | API returns seeded services and stop times |
| 28 | Month 1 review: clean clone, migration, seed, API docs, CI | `review` | Another developer can reproduce Month 1 demo |

---

### Milestone: Month 2 — Auth, Search & Passenger Portal

#### Week 5: Identity & Access Control

| Day | Title | Labels | Done when |
|---|---|---|---|
| 29 | Design User, Role, audit-event schema; access matrix | `backend`, `auth`, `design` | Roles and permissions agreed and documented |
| 30 | User and Role models, migrations, seed roles | `backend`, `auth`, `database` | Roles exist after migration/seed |
| 31 | Secure password hashing and registration endpoint | `backend`, `auth` | Password never stored/returned in plain text |
| 32 | Login and short-lived JWT access tokens | `backend`, `auth` | Valid login returns usable access token |
| 33 | Refresh token rotation, logout/revocation, expiry handling | `backend`, `auth` | Revoked/expired tokens cannot access protected endpoints |
| 34 | Role dependency/guards; protect administrative routes | `backend`, `auth` | Wrong roles receive HTTP 403 |
| 35 | Auth test suite, rate-limit login, document auth flow | `backend`, `auth`, `testing` | Positive and negative auth tests pass |

#### Week 6: Frontend Foundation

| Day | Title | Labels | Done when |
|---|---|---|---|
| 36 | React/Vite/TypeScript project and dev scripts | `frontend`, `setup` | `npm run dev` starts the application |
| 37 | ESLint, Prettier, unit-test runner, path aliases, env vars | `frontend` | Lint and frontend test commands pass |
| 38 | Base layout, navigation, theme tokens, buttons/forms, responsive shell | `frontend`, `design` | Desktop and mobile shell render correctly |
| 39 | Typed API client and query/error-state foundation | `frontend`, `api` | Client calls health endpoint successfully |
| 40 | Registration and login forms with client-side validation | `frontend`, `auth` | User can register/login through UI |
| 41 | Token persistence, protected routes, logout, session-expired handling | `frontend`, `auth` | Unauthenticated users cannot view private pages |
| 42 | Review: accessibility, mobile layout, auth integration | `frontend`, `review` | Authenticated dashboard shell is demo-ready |

#### Week 7: Journey Search Backend

| Day | Title | Labels | Done when |
|---|---|---|---|
| 43 | Search request/response contract; direct journey rules | `backend`, `search`, `design` | API contract in OpenAPI and docs |
| 44 | Origin/destination/date validation and station lookup | `backend`, `search` | Invalid or identical stations return useful errors |
| 45 | Direct-service search using ordered service stops | `backend`, `search` | Only trains reaching destination after origin appear |
| 46 | Schedule calculations: departure, arrival, duration, class summary | `backend`, `search` | Search results show accurate computed timing |
| 47 | Fare calculation rules for the synthetic network | `backend`, `search` | Same search returns deterministic class fares |
| 48 | Pagination, sorting, caching design, complete API tests | `backend`, `search`, `testing` | Search handles empty, valid, and boundary cases |
| 49 | Document search limitations; test query performance | `backend`, `search`, `docs` | Search is reliable and documented |

#### Week 8: Journey Search Frontend

| Day | Title | Labels | Done when |
|---|---|---|---|
| 50 | Search form: origin, destination, date, class controls | `frontend`, `search` | Form validates required inputs |
| 51 | Station autocomplete/swap and recent-search state | `frontend`, `search` | User can choose and swap stations easily |
| 52 | Search results cards: timing, duration, class, fare, availability | `frontend`, `search` | Results match backend response |
| 53 | Result filters/sort controls and route details drawer/page | `frontend`, `search` | User can inspect stops and service details |
| 54 | Loading, empty, offline, and API error states | `frontend`, `search` | UI never fails silently |
| 55 | Component tests, responsive/accessibility checks for search | `frontend`, `testing` | Main search path has automated UI tests |
| 56 | Month 2 review: demo register → login → journey search | `review` | Core passenger discovery experience complete |

---

### Milestone: Month 3 — Booking, PNR & Inventory

#### Week 9: Booking Domain & Inventory

| Day | Title | Labels | Done when |
|---|---|---|---|
| 57 | Design booking ERD and lifecycle state diagram | `backend`, `booking`, `design` | Booking states and transitions documented |
| 58 | Booking, Traveller, Ticket, Fare, PaymentAttempt models/migrations | `backend`, `booking`, `database` | DB stores complete purchase record |
| 59 | Service-date seat inventory and booking status constraints | `backend`, `booking`, `database` | Inventory is unique per service and seat |
| 60 | PNR format and collision-safe generator | `backend`, `booking` | PNR uniqueness protected at database level |
| 61 | Simulated payment states and idempotency-key policy | `backend`, `booking` | Retry behaviour explicitly documented |
| 62 | Seed service-date inventory; build availability query | `backend`, `booking`, `data` | Search can report sellable seats by class |
| 63 | Inventory/domain tests; transactional boundary review | `backend`, `booking`, `testing` | Inventory rules test-covered before booking API |

#### Week 10: Safe Booking APIs

| Day | Title | Labels | Done when |
|---|---|---|---|
| 64 | Booking quote endpoint with fare, class, availability recheck | `backend`, `booking`, `api` | Quote cannot be used for invalid journey |
| 65 | Atomic seat assignment using PostgreSQL row locking | `backend`, `booking`, `api` | One transaction allocates one available seat safely |
| 66 | Create-booking endpoint with traveller validation and PNR generation | `backend`, `booking`, `api` | Successful call returns confirmed booking/ticket data |
| 67 | Idempotency handling for repeated booking submissions | `backend`, `booking`, `api` | Repeating same request doesn't create another booking |
| 68 | Simulated payment confirmation/failure flow | `backend`, `booking`, `api` | Failed payment releases held allocation safely |
| 69 | Booking detail, passenger booking list, public PNR lookup | `backend`, `booking`, `api` | Correctly authorized retrieval paths work |
| 70 | Concurrency/integration and transaction-failure tests | `backend`, `booking`, `testing` | Parallel requests cannot double-book a seat |

#### Week 11: Booking Frontend

| Day | Title | Labels | Done when |
|---|---|---|---|
| 71 | Route from selected search result to booking flow | `frontend`, `booking` | Selected journey remains available in booking UI |
| 72 | Traveller-details form with validation and add/remove actions | `frontend`, `booking` | Invalid passenger details cannot be submitted |
| 73 | Class/seat selection UI using live availability | `frontend`, `booking` | User can choose only a valid available seat |
| 74 | Quote review and simulated payment confirmation page | `frontend`, `booking` | Repeat click is disabled/idempotent |
| 75 | Booking-success page with PNR, ticket details, print layout | `frontend`, `booking` | Completed booking is understandable and printable |
| 76 | My Bookings page and PNR lookup page | `frontend`, `booking` | Passenger can retrieve existing booking |
| 77 | UI tests and manual mobile/browser test of full booking flow | `frontend`, `booking`, `testing` | Search-to-confirmation succeeds reliably |

#### Week 12: Cancellation, RAC & Waitlist

| Day | Title | Labels | Done when |
|---|---|---|---|
| 78 | Define cancellation policy, refund simulation, RAC/waitlist rules | `backend`, `booking`, `design` | Rules written before implementation |
| 79 | Cancellation transaction and inventory release | `backend`, `booking` | Cancelling confirmed booking returns seat to inventory |
| 80 | RAC and waitlist assignment when confirmed capacity is full | `backend`, `booking` | Overflow bookings receive correct status/order |
| 81 | Promotion queue after cancellation with audit records | `backend`, `booking` | Next eligible booking promoted exactly once |
| 82 | Cancellation and refund-status UI | `frontend`, `booking` | Passenger can cancel eligible booking |
| 83 | RAC/waitlist status and promotion updates in booking views | `frontend`, `booking` | User understands their current booking state |
| 84 | Month 3 review: booking, cancellation, promotion end-to-end | `review` | Booking integrity is the project's strongest-tested workflow |

---

### Milestone: Month 4 — Operations & Live Status

#### Week 13: Operational Data & Permissions

| Day | Title | Labels | Done when |
|---|---|---|---|
| 85 | Design service-status, delay-event, platform-allocation, location-update models | `backend`, `operations`, `design` | Operations ERD and state transitions documented |
| 86 | Status and delay models/migrations with audit ownership | `backend`, `operations`, `database` | Every update records who made it and when |
| 87 | Platform allocation and occupancy conflict validation | `backend`, `operations` | Two services cannot claim same platform/time window |
| 88 | Simulated location-update endpoint restricted to operations roles | `backend`, `operations`, `api` | Passenger role cannot submit location data |
| 89 | Service-status timeline and latest-location query APIs | `backend`, `operations`, `api` | API returns ordered, clear current status |
| 90 | Safe simulation script for route-based train location/status updates | `backend`, `operations` | Local demo can create changing train state |
| 91 | Permission, validation, and operational API tests | `backend`, `operations`, `testing` | Invalid status/platform/location updates rejected |

#### Week 14: Real-Time Delivery & Passenger Status

| Day | Title | Labels | Done when |
|---|---|---|---|
| 92 | Redis client and update channel/message schema | `backend`, `realtime` | Backend can publish/consume a test message |
| 93 | WebSocket connection lifecycle and authenticated subscription rules | `backend`, `realtime` | Clients connect only to allowed channels |
| 94 | Publish booking/service status changes through Redis/WebSocket | `backend`, `realtime` | Update reaches subscribed browser clients |
| 95 | Polling fallback and reconnect/backoff behaviour | `backend`, `realtime` | Status remains usable after temporary disconnect |
| 96 | Passenger train-status page with location, delay, stop timeline | `frontend`, `realtime` | Passenger can track a seeded service |
| 97 | Live-update indicators, accessible announcements, error/offline UX | `frontend`, `realtime` | User can tell whether data is live or stale |
| 98 | Real-time integration tests and simulated-data limitation docs | `backend`, `realtime`, `testing` | WebSocket path is testable and transparent |

#### Week 15: Operations Dashboard

| Day | Title | Labels | Done when |
|---|---|---|---|
| 99 | Dashboard information architecture for Station Master and Operations Manager | `frontend`, `operations`, `design` | Wireframes identify role-specific actions |
| 100 | Train board: service status, delay, platform, last update, filtering | `frontend`, `operations` | Operations user can find a service quickly |
| 101 | Service-detail workspace with status timeline and location history | `frontend`, `operations` | Staff can inspect one service fully |
| 102 | Delay/status update form with reason, validation, audit confirmation | `frontend`, `operations` | Authorized staff can make an operational update |
| 103 | Platform occupancy board and conflict explanation | `frontend`, `operations` | Staff can see and resolve allocation conflicts |
| 104 | Dashboard live updates, role tests, responsive layout | `frontend`, `operations` | Changes appear without a manual refresh |
| 105 | Operations workflow demo; fix high-priority usability defects | `frontend`, `operations`, `review` | Update → passenger notification path works |

#### Week 16: Core-Release Hardening

| Day | Title | Labels | Done when |
|---|---|---|---|
| 106 | Backend/frontend Dockerfiles; integrate app services into Compose | `devops` | Full stack starts with one Compose command |
| 107 | Production env validation, CORS, health/readiness checks, safe logging | `devops`, `backend` | Misconfiguration fails safely and clearly |
| 108 | End-to-end tests: register, search, booking, cancellation, live status | `testing` | Main user journey is automated |
| 109 | Accessibility audit, responsive polish, keyboard-navigation fixes | `frontend`, `a11y` | Critical flows work without a mouse |
| 110 | API reference, ERD, architecture diagram, setup guide, user manual | `docs` | Documentation supports independent setup |
| 111 | Scripted demo dataset; demo story: search → book → track → operate | `data`, `docs` | Demo works consistently from clean database |
| 112 | Release checklist, tag `v1.0.0`, known limitations, Months 5-6 backlog | `release` | Core RailwayOS release is reproducible and portfolio-ready |
