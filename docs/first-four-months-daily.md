# RailwayOS: Day-by-Day Plan for Months 1-4

This is the implementation plan for the core release. Work in order. At the start of a session, say: **“RailwayOS Day N”** and describe what you completed; we will continue from that day's checklist.

## Definition of done every day

- Code is formatted and tests relevant to the change pass.
- Update the README or API documentation if behaviour changed.
- Commit using `day-NNN: short description`.
- Record blockers in the issue board or daily note.

## Month 1 — Foundation and railway data

### Week 1: Development foundation

| Day | Task | Done when |
| --- | --- | --- |
| 1 | Read the roadmap; create GitHub issues/milestones for Months 1-4; verify prerequisites. | The issue board has the four monthly milestones. |
| 2 | Copy `.env.example` to local `.env`; set safe development passwords; validate Docker configuration. | `docker compose config` succeeds and `.env` is ignored. |
| 3 | Start PostgreSQL and Redis using Docker; check health, ports, and persisted volumes. | Both containers report healthy. |
| 4 | Create backend Python virtual environment and dependency manifest. | A clean environment can install backend dependencies. |
| 5 | Create FastAPI application package and `GET /health`. | The API starts and health returns HTTP 200. |
| 6 | Add pytest, a health endpoint test, formatter, linter, and pre-commit configuration. | Test, format, and lint commands pass. |
| 7 | Add GitHub Actions workflow for backend checks and write local setup instructions. | Push/PR CI runs the same basic checks. |

### Week 2: Backend architecture

| Day | Task | Done when |
| --- | --- | --- |
| 8 | Create application settings with `pydantic-settings` and environment validation. | App reads configuration without hard-coded secrets. |
| 9 | Add API prefix/versioning, router structure, and OpenAPI metadata. | Swagger groups endpoints under `/api/v1`. |
| 10 | Add request IDs, structured logging, and a global error response format. | Invalid API request returns a consistent JSON error. |
| 11 | Configure SQLAlchemy engine/session and database connectivity check. | Backend connects to PostgreSQL locally. |
| 12 | Initialize Alembic and create a blank migration workflow. | `alembic upgrade head` runs successfully. |
| 13 | Add database test fixture strategy and separate test database configuration. | Tests do not use or damage development data. |
| 14 | Review Week 2: refactor imports, document architecture decisions, and run full checks. | Fresh backend setup and checks pass. |

### Week 3: Core railway schema

| Day | Task | Done when |
| --- | --- | --- |
| 15 | Design ERD for stations, trains, routes, services, stops, coaches, and seats. | ERD is committed in `docs/`. |
| 16 | Implement Station model, migration, schemas, and validation. | Station table migrates and tests pass. |
| 17 | Implement Train and Coach models with train-number constraints. | Train/coaches migrate with valid relations. |
| 18 | Implement Route and RouteStop models with ordered stops and distances. | Route stop order is enforced by constraints/application rules. |
| 19 | Implement TrainService and ServiceStop models for a dated timetable. | A service can represent a train on a specific date. |
| 20 | Implement Seat model, seat class, and coach-seat uniqueness. | No coach can contain duplicate seat numbers. |
| 21 | Write model and migration tests; create a schema reference document. | All core-model tests pass. |

### Week 4: Seed data and public APIs

| Day | Task | Done when |
| --- | --- | --- |
| 22 | Define a small synthetic network: 10-20 stations and 5-10 train services. | Dataset assumptions are documented. |
| 23 | Build idempotent seed command for stations and routes. | Re-running the command creates no duplicates. |
| 24 | Extend seeds for trains, coaches, seats, services, and stop times. | A fresh database contains a usable timetable. |
| 25 | Build read-only station list/detail APIs with search and pagination. | API tests cover list, search, and missing station. |
| 26 | Build train and route detail APIs. | A route response contains ordered stops. |
| 27 | Build timetable/service detail APIs. | API returns the seeded services and stop times. |
| 28 | Month 1 review: verify clean clone, migration, seed, API docs, and CI. | Another developer could reproduce the Month 1 demo. |

## Month 2 — Authentication, search, and passenger portal

### Week 5: Identity and access control

| Day | Task | Done when |
| --- | --- | --- |
| 29 | Design User, Role, and audit-event schema; document access matrix. | Roles and permissions are agreed and documented. |
| 30 | Add User and Role models, migrations, and seed roles. | Roles exist after migration/seed. |
| 31 | Implement secure password hashing and registration endpoint. | Password is never stored or returned in plain text. |
| 32 | Implement login and short-lived JWT access tokens. | Valid login returns a usable access token. |
| 33 | Add refresh token rotation, logout/revocation, and expiry handling. | Revoked/expired tokens cannot access protected endpoints. |
| 34 | Add role dependency/guards and protect administrative routes. | Wrong roles receive HTTP 403. |
| 35 | Add auth test suite, rate-limit login, and document auth flow. | Positive and negative auth tests pass. |

### Week 6: Frontend foundation

| Day | Task | Done when |
| --- | --- | --- |
| 36 | Create React/Vite/TypeScript frontend project and development scripts. | `npm run dev` starts the application. |
| 37 | Configure ESLint, Prettier, unit-test runner, path aliases, and environment variables. | Lint and frontend test commands pass. |
| 38 | Build base layout, navigation, theme tokens, reusable buttons/forms, and responsive shell. | Desktop and mobile shell render correctly. |
| 39 | Build typed API client and query/error-state foundation. | Client calls the health endpoint successfully. |
| 40 | Build registration and login forms with client-side validation. | User can register/login through the UI. |
| 41 | Add token persistence, protected routes, logout, and session-expired handling. | Unauthenticated users cannot view private pages. |
| 42 | Review frontend accessibility, mobile layout, and auth integration. | Authenticated dashboard shell is demo-ready. |

### Week 7: Journey search backend

| Day | Task | Done when |
| --- | --- | --- |
| 43 | Specify search request/response contract and rules for direct journeys. | API contract is in OpenAPI and docs. |
| 44 | Implement origin/destination/date validation and station lookup. | Invalid or identical stations return useful errors. |
| 45 | Implement direct-service search using ordered service stops. | Only trains that reach destination after origin appear. |
| 46 | Add schedule calculations: departure, arrival, duration, and available class summary. | Search results show accurate computed timing. |
| 47 | Add fare calculation rules for the synthetic network. | Same search returns deterministic class fares. |
| 48 | Add pagination, sorting, caching design, and complete API tests. | Search handles empty, valid, and boundary cases. |
| 49 | Document search limitations; test query performance with the seed dataset. | Search is reliable and documented. |

### Week 8: Journey search frontend

| Day | Task | Done when |
| --- | --- | --- |
| 50 | Build search form with accessible origin, destination, date, and class controls. | Form validates required inputs. |
| 51 | Add station autocomplete/swap control and recent-search state. | User can choose and swap stations easily. |
| 52 | Build search results cards with timing, duration, class, fare, and availability. | Results match the backend response. |
| 53 | Build result filters/sort controls and route details drawer/page. | User can inspect stops and service details. |
| 54 | Add loading, empty, offline, and API error states. | UI never fails silently. |
| 55 | Add component tests and responsive/accessibility checks for search. | Main search path has automated UI tests. |
| 56 | Month 2 review: demo registration → login → journey search. | Core passenger discovery experience is complete. |

## Month 3 — Booking, PNR, and inventory correctness

### Week 9: Booking domain and inventory

| Day | Task | Done when |
| --- | --- | --- |
| 57 | Design booking ERD and lifecycle state diagram. | Booking states and allowed transitions are documented. |
| 58 | Add Booking, Traveller, Ticket, Fare, and PaymentAttempt models/migrations. | Database stores the complete purchase record. |
| 59 | Add service-date seat inventory and booking status constraints. | Inventory is unique per service and seat. |
| 60 | Create PNR format and collision-safe generator. | PNR uniqueness is protected at database level. |
| 61 | Define simulated payment states and idempotency-key policy. | Retry behaviour is explicitly documented. |
| 62 | Seed service-date inventory and build availability query. | Search can report sellable seats by class. |
| 63 | Write inventory/domain tests and review transactional boundaries. | Inventory rules are test-covered before booking API work. |

### Week 10: Safe booking APIs

| Day | Task | Done when |
| --- | --- | --- |
| 64 | Create booking quote endpoint with fare, class, and availability recheck. | Quote cannot be used for an invalid journey. |
| 65 | Implement atomic seat assignment using PostgreSQL row locking. | One transaction allocates one available seat safely. |
| 66 | Implement create-booking endpoint with traveller validation and PNR generation. | Successful call returns confirmed booking/ticket data. |
| 67 | Add idempotency handling for repeated booking submissions. | Repeating same request does not create another booking. |
| 68 | Implement simulated payment confirmation/failure flow. | Failed payment releases held allocation safely. |
| 69 | Add booking detail, passenger booking list, and public PNR lookup endpoints. | Correctly authorized retrieval paths work. |
| 70 | Write concurrency/integration tests and transaction-failure tests. | Parallel requests cannot double-book a seat. |

### Week 11: Booking frontend

| Day | Task | Done when |
| --- | --- | --- |
| 71 | Add route from selected search result to booking flow. | Selected journey remains available in booking UI. |
| 72 | Build traveller-details form with validation and add/remove traveller actions. | Invalid passenger details cannot be submitted. |
| 73 | Build class/seat selection UI using live availability. | User can choose only a valid available seat. |
| 74 | Build quote review and simulated payment confirmation page. | Repeat click is disabled/idempotent. |
| 75 | Build booking-success page with PNR, ticket details, and print-friendly layout. | A completed booking is understandable and printable. |
| 76 | Build My Bookings page and PNR lookup page. | Passenger can retrieve an existing booking. |
| 77 | Add UI tests and manual mobile/browser test of full booking flow. | Search-to-confirmation succeeds reliably. |

### Week 12: Cancellation, RAC, and waitlist

| Day | Task | Done when |
| --- | --- | --- |
| 78 | Define cancellation policy, refund simulation, and RAC/waitlist promotion rules. | Rules are written before implementation. |
| 79 | Implement cancellation transaction and inventory release. | Cancelling confirmed booking returns its seat to inventory. |
| 80 | Implement RAC and waitlist assignment when confirmed capacity is full. | Overflow bookings receive correct status/order. |
| 81 | Implement promotion queue after cancellation with audit records. | Next eligible booking is promoted exactly once. |
| 82 | Build cancellation and refund-status UI. | Passenger can cancel eligible booking. |
| 83 | Show RAC/waitlist status and promotion updates in booking views. | User understands their current booking state. |
| 84 | Month 3 review: test booking, cancellation, and promotion end-to-end. | Booking integrity is the project’s strongest-tested workflow. |

## Month 4 — Operations and live status

### Week 13: Operational data and permissions

| Day | Task | Done when |
| --- | --- | --- |
| 85 | Design service-status, delay-event, platform-allocation, and location-update models. | Operations ERD and state transitions are documented. |
| 86 | Implement status and delay models/migrations with audit ownership. | Every update records who made it and when. |
| 87 | Implement platform allocation and occupancy conflict validation. | Two services cannot claim same platform/time window. |
| 88 | Implement simulated location-update endpoint restricted to operations roles. | Passenger role cannot submit location data. |
| 89 | Implement service-status timeline and latest-location query APIs. | API returns an ordered, clear current status. |
| 90 | Build a safe simulation script to emit route-based train location/status updates. | Local demo can create changing train state. |
| 91 | Add permission, validation, and operational API tests. | Invalid status/platform/location updates are rejected. |

### Week 14: Real-time delivery and passenger status

| Day | Task | Done when |
| --- | --- | --- |
| 92 | Configure Redis client and define update channel/message schema. | Backend can publish/consume a test message. |
| 93 | Implement WebSocket connection lifecycle and authenticated subscription rules. | Clients connect only to allowed channels. |
| 94 | Publish booking/service status changes through Redis/WebSocket. | An update reaches subscribed browser clients. |
| 95 | Add polling fallback and reconnect/backoff behaviour. | Status remains usable after temporary disconnect. |
| 96 | Build passenger train-status page with current location, delay, and stop timeline. | Passenger can track a seeded service. |
| 97 | Add live-update indicators, accessible announcements, and error/offline UX. | User can tell whether data is live or stale. |
| 98 | Write real-time integration tests and document simulated-data limitation. | WebSocket path is testable and transparent. |

### Week 15: Operations dashboard

| Day | Task | Done when |
| --- | --- | --- |
| 99 | Design dashboard information architecture for Station Master and Operations Manager. | Wireframes identify role-specific actions. |
| 100 | Build train board: service status, delay, platform, last update, and filtering. | Operations user can find a service quickly. |
| 101 | Build service-detail workspace with status timeline and location history. | Staff can inspect one service fully. |
| 102 | Build delay/status update form with reason, validation, and audit confirmation. | Authorized staff can make an operational update. |
| 103 | Build platform occupancy board and conflict explanation. | Staff can see and resolve allocation conflicts. |
| 104 | Add dashboard live updates, role tests, and responsive layout. | Changes appear without a manual refresh. |
| 105 | Conduct an operations workflow demo and fix high-priority usability defects. | Update → passenger notification path works. |

### Week 16: Core-release hardening

| Day | Task | Done when |
| --- | --- | --- |
| 106 | Add backend/frontend Dockerfiles and integrate application services into Compose. | Full stack starts with one Compose command. |
| 107 | Add production-style environment validation, CORS rules, health/readiness checks, and safe logging. | Misconfiguration fails safely and clearly. |
| 108 | Add end-to-end tests for register, search, booking, cancellation, and live status. | Main user journey is automated. |
| 109 | Perform accessibility audit, responsive polish, and keyboard-navigation fixes. | Critical flows work without a mouse. |
| 110 | Complete API reference, ERD, architecture diagram, setup guide, and user manual. | Documentation supports independent setup. |
| 111 | Prepare scripted demo dataset and demo story: search → book → track → operate. | Demo works consistently from a clean database. |
| 112 | Run release checklist, tag `v1.0.0`, capture known limitations, and create Months 5-6 backlog. | Core RailwayOS release is reproducible and portfolio-ready. |

## When you return each day

Send the day number and any command output or error. For example: `RailwayOS Day 5 — FastAPI starts, but my health test fails.` I will then help you complete only that day’s task, verify it, and prepare the next day.
