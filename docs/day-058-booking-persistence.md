# Day 58 — Booking persistence

## Implementation

- Added SQLAlchemy models for `Booking`, `Traveller`, `Ticket`, `Fare`, and
  `PaymentAttempt`.
- Added booking and payment status enums, foreign keys to identity, services,
  seats, and stations, monetary snapshots, timestamps, and purchase-record
  indexes.
- Added Alembic revision `20261126_01_create_booking.py` with reversible
  creation and downgrade of all five tables.
- Added model registration and tests for table metadata, defaults, and unique
  constraints.

The booking API and seat inventory allocation remain separate follow-up work;
this day makes the complete purchase record persistable without claiming that
booking is already exposed to passengers.

## Verification

```powershell
python -m pytest
alembic heads
npm.cmd run build
npm.cmd run lint
```
