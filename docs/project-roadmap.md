# RailwayOS: Six-Month Major-Project Roadmap

RailwayOS is a simulated railway operations platform. It is designed as a credible portfolio and academic major project: it solves real operational workflows while using synthetic data and clearly avoiding claims of connection to production railway systems.

## Project outcome

At the end of Month 4, RailwayOS will provide a working core system for:

- passenger journey search, booking, PNR lookup, cancellation, RAC, and waitlist;
- train schedules, seat inventory, and simulated live train location;
- role-based operational tools for station and operations staff; and
- a responsive web application, documented API, seeded demo data, tests, and Docker deployment.

Months 5 and 6 turn that core into a stronger major project through analytics, explainable ML, reliability, security, and a polished demonstration.

## Non-negotiable product boundaries

- Use only synthetic, public, or explicitly permitted data.
- Treat every live-location feed and payment action as simulated unless an approved integration is added.
- Do not position the application as an official railway system or safety-critical dispatch platform.
- Build a modular monolith first: FastAPI, PostgreSQL, Redis, React, and WebSockets. This is practical to develop, test, and deploy.

## Delivery rhythm

Each week has five build days, one test/documentation day, and one buffer day. Every completed week should end with a demo, tests, an updated README, and a small Git commit series.

The complete daily checklist for the core release is in [First Four Months: Day-by-Day Plan](first-four-months-daily.md).

---

## Months 1-4: Core working product

### Month 1 — Platform, data model, and public information

**Goal:** establish a reliable developer platform and model the railway network.

| Week | Work | Demonstrable result |
| --- | --- | --- |
| 1 | Confirm scope; set up local Docker, Python, Node, formatting, linting, CI, environment handling, and issue board. | A fresh clone starts the database and cache; CI runs basic checks. |
| 2 | Bootstrap FastAPI, settings, structured errors, logging, health/readiness endpoints, tests, and API versioning. | Documented `GET /health` endpoint with test coverage. |
| 3 | Set up PostgreSQL, SQLAlchemy, Alembic, and core schema: stations, trains, routes, services, stops, coaches, and seats. | A migration creates the model from an empty database. |
| 4 | Add a consistent synthetic network dataset and read-only APIs for stations, routes, train services, and timetables. | Users can browse a realistic sample network through Swagger/API. |

**Month 1 acceptance:** clean setup instructions, reproducible database migration/seed process, CI checks, and an API that returns train and schedule data.

### Month 2 — Identity, search, and passenger portal

**Goal:** allow passengers to securely find suitable journeys.

| Week | Work | Demonstrable result |
| --- | --- | --- |
| 5 | Build user accounts, password hashing, JWT sessions, refresh/logout flow, and RBAC. | Passenger and staff roles can authenticate; protected APIs reject invalid access. |
| 6 | Create React application shell, design system, router, API client, auth screens, and guarded routes. | A user can register, sign in, and access the right dashboard. |
| 7 | Implement journey search: origin, destination, date, stops, fare class, duration, and available seats. | Search returns valid direct journeys from the seeded timetable. |
| 8 | Build search and results UI, journey details, error/empty states, and mobile layout. | Passenger can complete an end-to-end search in the browser. |

**Month 2 acceptance:** a responsive authenticated passenger portal with tested journey search against the real project database.

### Month 3 — Booking, PNR, and inventory correctness

**Goal:** deliver the highest-value workflow without double-booking seats.

| Week | Work | Demonstrable result |
| --- | --- | --- |
| 9 | Add booking, traveller, ticket, fare, payment-simulation, and audit-log entities. | Database supports a full booking lifecycle. |
| 10 | Implement seat availability, seat selection, atomic booking transaction, PNR generator, and idempotency protection. | Concurrent booking tests prove a seat cannot be allocated twice. |
| 11 | Build booking UI: traveller form, seat selection, simulated payment confirmation, ticket view, and booking history. | A passenger can search and book a ticket with a generated PNR. |
| 12 | Add cancellation, refund simulation, RAC/waitlist states, and waitlist promotion after cancellation. | Booking lifecycle tests cover confirm, cancel, release, and promote states. |

**Month 3 acceptance:** full passenger journey from registration through cancellation, supported by unit and integration tests for allocation rules.

### Month 4 — Operations and live-status experience

**Goal:** make the project useful beyond a booking clone by adding operational visibility.

| Week | Work | Demonstrable result |
| --- | --- | --- |
| 13 | Model service status, delay events, platform allocation, and simulated GPS/location updates. | Operations staff can update a train’s current status. |
| 14 | Add WebSocket notifications (with polling fallback), Redis pub/sub, and passenger live-status screen. | A simulated update reaches the browser without a refresh. |
| 15 | Build operations dashboard: train board, delay entry, platform occupancy, and service detail views. | Operations role can monitor and update multiple services. |
| 16 | Add dashboards, end-to-end tests, accessibility pass, Docker deployment, demo data, API documentation, and user manual. | Version `v1.0.0` is demo-ready from a clean environment. |

**Month 4 acceptance (Core Release):** working Docker deployment, passenger and operations workflows, seeded demo dataset, tests, architecture diagram, API docs, and a recorded or scripted demo.

---

## Months 5-6: Make it a solid major project

### Month 5 — Analytics and explainable intelligence

**Goal:** add features with clear operational value, only after the core data pipeline is stable.

| Week | Work | Demonstrable result |
| --- | --- | --- |
| 17 | Create analytics event model and reporting queries for bookings, occupancy, cancellations, and delays. | Admin dashboard shows operational KPIs. |
| 18 | Build synthetic historical dataset generator and document data assumptions. | Reproducible datasets support model experiments without private data. |
| 19 | Train and serve a baseline delay-prediction model; record metrics and model version. | Service predicts delay risk for a selected service. |
| 20 | Add explainability, confidence/limitations display, and waitlist-confirmation probability only if metrics justify it. | UI explains factors affecting a prediction and warns users of uncertainty. |

**Month 5 acceptance:** documented, reproducible, non-safety-critical predictive feature with evaluation metrics and clear limitations.

### Month 6 — Production quality and project defence

**Goal:** harden the system and prepare a professional final submission.

| Week | Work | Demonstrable result |
| --- | --- | --- |
| 21 | Security review: validation, CORS, rate limiting, token handling, secrets management, audit logs, and dependency scan. | Security checklist and negative-path tests are complete. |
| 22 | Reliability work: monitoring endpoint, structured logs, backups/migration procedure, cache invalidation, load and failure tests. | System behaviour under expected failure cases is documented. |
| 23 | Improve UX: accessibility, performance, responsive layout, error recovery, notifications, and demo polish. | Lighthouse/accessibility issues are resolved or documented. |
| 24 | Complete final report, architecture diagrams, ERD, test report, installation guide, demo video/script, backlog, and release `v2.0.0`. | A reviewer can install, test, understand, and demonstrate the project independently. |

**Month 6 acceptance:** a portfolio-ready major project with a credible technical report and reproducible demonstration.

## Feature priority

| Must have by Month 4 | Should have by Month 6 | Future backlog |
| --- | --- | --- |
| Auth/RBAC, timetable search, booking, PNR, cancellation, RAC/waitlist, seat integrity, live simulated status, operations dashboard | Analytics, delay-risk model, audit trail, notifications, CI/CD, monitoring, performance/security testing | Real carrier feeds, payment gateway, SMS/email provider, multilingual support, cargo, maintenance prediction, LLM assistant |

## How to start this week

1. Set up the project board with Week 1 issues from this document.
2. Copy `.env.example` to `.env`; replace all development passwords locally and never commit it.
3. Verify `docker compose config` succeeds.
4. Begin Week 1 with tooling and CI; do not begin the frontend before the backend health endpoint and database workflow are reproducible.

## Success metrics

- A new developer can run the system locally using the documentation.
- Passenger booking and cancellation paths have automated tests, including concurrent seat allocation.
- Role checks protect passenger and operations functions.
- Live updates and AI/analytics are visibly simulated and explain their limitations.
- The final demo tells one coherent story: search → book → track → operate → analyze.
