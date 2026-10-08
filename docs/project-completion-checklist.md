# RailwayOS project completion checklist

This document is the working checklist for taking RailwayOS from its current
foundation to a complete portfolio-ready release. Each item should be finished,
tested, documented, and committed before moving to the next item.

## Current baseline

- [x] Core backend structure and health checks
- [x] Railway network models and migrations
- [x] Synthetic seed data
- [x] Station, train, route, and service APIs
- [x] User, role, and identity foundation
- [x] Password hashing and registration foundation
- [x] Authentication design and API contract
- [x] Login endpoint and short-lived JWT access tokens

## Phase 1 — Authentication completion

- [x] Implement `POST /api/v1/auth/login`.
- [x] Normalize email addresses before lookup.
- [x] Reject invalid and inactive users with a generic `401` response.
- [x] Create signed JWT access tokens with explicit expiry claims.
- [x] Add tests for successful login, invalid password, unknown email, and
      inactive users.
- [x] Document local authentication verification.

## Phase 2 — Session and authorization

- [ ] Implement refresh-token rotation and revocation.
- [ ] Implement logout and expired-token handling.
- [ ] Add authenticated-user dependencies.
- [ ] Add role guards to administrative endpoints.
- [ ] Add audit events for authentication and protected actions.

## Phase 3 — Passenger journey search

- [ ] Define search request and response schemas.
- [ ] Validate origin, destination, and travel date.
- [ ] Return direct services with ordered stops.
- [ ] Calculate departure, arrival, duration, and fares.
- [ ] Add pagination, deterministic sorting, and API tests.

## Phase 4 — Booking workflow

- [ ] Add inventory availability checks.
- [ ] Create booking and passenger models.
- [ ] Reserve seats transactionally.
- [ ] Add booking retrieval, cancellation, and PNR lookup.
- [ ] Prevent duplicate or conflicting reservations.

## Phase 5 — Frontend

- [ ] Create the React/Vite/TypeScript application shell.
- [ ] Add login, registration, logout, and protected routes.
- [ ] Add station and journey search screens.
- [ ] Add booking and passenger views.
- [ ] Add responsive layout and accessibility checks.

## Phase 6 — Release readiness

- [ ] Run backend and frontend tests from a clean checkout.
- [ ] Run formatting, linting, and type checks.
- [ ] Validate migrations and seed data in a fresh database.
- [ ] Update README and local setup documentation.
- [ ] Verify CI on a pull request.
- [ ] Tag the first portfolio-ready release.

## Definition of complete

RailwayOS is complete for the first release when a new developer can clone the
repository, configure the environment, migrate and seed a database, start the
backend and frontend, register and log in, search for a journey, and complete a
safe demo booking with automated checks passing.
