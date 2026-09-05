# Contributing to RailwayOS

This project follows a day-by-day development plan across 112 days.
Each day produces at least one commit following the format: `day-NNN: short description`.

## Day-by-Day Workflow

1. Open `docs/first-four-months-daily.md` and find today's task.
2. Do the work described in the task.
3. Verify using the "Done when" criterion.
4. Commit with the standard format: `day-NNN: description`.
5. Record any blockers in the issue board.

## Commit Format

```
day-NNN: short description of what was done

Optional body explaining:
- Why this approach was chosen
- What was validated
- What the next step depends on
```

**Examples:**
```
day-002: add .env from template; validate docker compose config
day-005: add FastAPI app with GET /health returning HTTP 200
day-012: init Alembic; blank migration runs successfully
```

## Definition of Done (Every Day)

- [ ] Code is formatted (`ruff format .`)
- [ ] Relevant tests pass (`pytest`)
- [ ] README/API docs updated if behaviour changed
- [ ] Committed using `day-NNN:` format
- [ ] Blockers recorded in issue board

## File Naming

| Type | Convention | Example |
|------|-----------|---------|
| Daily docs | `docs/day-NNN-slug.md` | `docs/day-002-env-and-docker.md` |
| Scripts | `scripts/verb_noun.py` | `scripts/validate_env.py` |
| Backend models | `backend/app/models/noun.py` | `backend/app/models/station.py` |
| Migrations | Alembic auto-generated | `alembic/versions/001_add_station.py` |

## Branch Strategy

For this portfolio project, all work goes directly to `main`.
Feature branches can be used for experimental work and merged via PR.

## Environment

Always work with a valid `.env` file:

```bash
cp .env.example .env
# Edit .env with dev passwords
python scripts/validate_env.py
```

Never commit `.env`. It is git-ignored by design.
