# Day 59 — Service-date inventory constraints

## Implementation

- Added `ServiceSeatInventory`, keyed by a dated `TrainService` and physical
  `Seat`.
- Enforced uniqueness for `(service_id, seat_id)` so one seat cannot receive
  two inventory records for the same service.
- Added explicit `AVAILABLE`, `HELD`, `SOLD`, and `BLOCKED` states plus an
  optional booking hold and expiry timestamp.
- Added nonnegative database checks for booking totals, ticket fares, fare
  snapshots, and payment attempts.
- Added reversible Alembic revision `20261126_02` and model tests.

Inventory allocation and availability queries remain Day 62 work; this change
establishes the persistence boundary and constraints they will use.

## Verification

```powershell
python -m pytest
alembic heads
npm.cmd run build
npm.cmd run lint
```
