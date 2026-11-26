# Day 60 — Collision-safe PNR generation

## Implementation

- Added the fixed ten-character `RO########` PNR format.
- Added bounded retry generation in `backend/app/services/pnr.py`.
- Existing candidates are checked before returning a PNR.
- `PNRGenerationError` makes retry exhaustion explicit.
- The `bookings.pnr` column remains database-unique through
  `uq_booking_pnr`, providing the final concurrent-insert guard.
- Added tests for format, collision retry, retry exhaustion, and database
  uniqueness/length.

The generator is ready for the booking creation service; booking API wiring is
outside Day 60.

## Verification

```powershell
python -m pytest
alembic heads
npm.cmd run build
npm.cmd run lint
```
