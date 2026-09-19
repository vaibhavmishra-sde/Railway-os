# Day 015 — Completion Note

**Date completed:** 2026-09-20  
**Plan reference:** Month 1 → Week 3 → Day 15  
**Commit prefix:** `day-015`

## Done

- [x] ERD design notes written (`docs/day-015-erd-design.md`)
- [x] Mermaid ERD committed (`docs/erd.md`) — all 8 entities with column types and relationships
- [x] Models package created (`backend/app/models/`)
  - `station.py` — `Station` model
  - `train.py` — `Train`, `Coach`, `SeatClass` enum
  - `seat.py` — `Seat`, `BerthType` enum
  - `route.py` — `Route`, `RouteStop`
  - `service.py` — `TrainService`, `ServiceStop`, `ServiceStatus` enum
  - `__init__.py` — re-exports all models for Alembic discovery
- [x] `migrations/env.py` updated to import `app.models`
- [x] Smoke tests added (`tests/test_models_day015.py`)
- [x] Architecture doc updated with Week 3 section and W3 ADRs
- [x] README updated (milestone, progress table, doc links)

## Verification checklist

```
"Done when": ERD is committed in docs/
```
✅ `docs/erd.md` — Mermaid ERD with all 8 entities  
✅ `docs/day-015-erd-design.md` — design rationale and attribute lists  
✅ All model files importable (verified by smoke tests)  
✅ SQLite DDL creation passes (`test_all_model_tables_created`)

## Next: Day 16

> Implement Station model, migration, schemas, and validation.  
> Done when: Station table migrates and tests pass.

Actions for Day 16:
1. Generate Alembic migration for `stations` table
2. Add Pydantic schemas for Station (request/response)
3. Add validation: code must be 3-5 uppercase alpha chars
4. Add CRUD helpers for Station
5. Write model and schema tests
