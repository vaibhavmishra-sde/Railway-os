# Day 022 — Synthetic Network Dataset

RailwayOS uses a fictional network so development and demonstrations do not
depend on private or production railway data.

## Dataset assumptions

- 12 stations represent a connected north-to-south corridor.
- Station codes are stable three-letter identifiers used by APIs and seeds.
- Routes contain at least three ordered stations and use synthetic distances.
- Services are dated timetable examples; all times are illustrative.
- The dataset is intentionally small enough for local development and tests.

The catalog is designed to be deterministic and safe to reseed. Future seed
commands must identify records by their stable codes rather than generated
UUIDs.

The code catalog currently contains 12 stations, 3 connected routes, and 5
dated service examples. It is exposed through `app.data.network` and checked
by `backend/tests/test_network_catalog.py` before seed-command work begins.
