# Day 57 — Booking invariants

These constraints guide Day 58 model and migration work.

- `Booking.pnr` is unique and generated only after a successful booking
  creation transaction.
- `Booking.idempotency_key` is unique per passenger and booking operation;
  replaying it returns the original result.
- A booking must contain at least one traveller and one ticket before it can
  enter `PAYMENT_PENDING`.
- A ticket belongs to exactly one booking and one traveller.
- A confirmed ticket can reference only a seat belonging to its service's
  train, and the same service/seat/date combination cannot be confirmed twice.
- Fare and route values on a ticket are snapshots; timetable edits do not
  rewrite historical tickets.
- Monetary values are stored as integer minor units with an explicit currency.
- Every status transition creates one append-only `BOOKING_EVENT` row.
- Cancellation and expiry are idempotent: repeating either command cannot
  release inventory or create a refund twice.
- Payment and refund providers are simulated; no real payment claim is made.
