# RailwayOS

A full-stack railway operations platform built as a portfolio project.

**Current milestone:** Day 15 complete — Week 3 started; ERD designed and all core ORM models (Station, Train, Coach, Seat, Route, RouteStop, TrainService, ServiceStop) committed.

## Progress

| Day | Task | Status |
|-----|------|--------|
| 1 | Read roadmap; create GitHub issues/milestones; verify prerequisites | Done |
| 2 | Copy `.env.example` to `.env`; set dev passwords; validate Docker config | Done |
| 3 | Start PostgreSQL + Redis via Docker; check health, ports, volumes | Done |
| 4 | Create backend Python virtual environment and dependency manifest | Done |
| 5 | Scaffold FastAPI app and local dev server | Done |
| 6 | Add backend tests, formatter, linter, and pre-commit checks | Done |
| 7 | Add GitHub Actions workflow for backend checks and write local setup instructions | Done |
| 8 | Create application settings with `pydantic-settings` and environment validation | Done |
| 9 | Add API prefix/versioning, router structure, and OpenAPI metadata | Done |
| 10 | Add request IDs, structured logging, and a global error response format | Done |
| 11 | Configure SQLAlchemy engine/session and database connectivity check | Done |
| 12 | Initialize Alembic and create a blank migration workflow | Done |
| 13 | Add database test fixture strategy and separate test database configuration | Done |
| 14 | Review Week 2: refactor imports, document architecture decisions, and run full checks | Done |
| 15 | Design ERD for stations, trains, routes, services, stops, coaches, and seats; commit model stubs | Done |

## Backend API

Start the application from the `backend` directory:

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

The liveness endpoint is available at `http://127.0.0.1:8000/health` and returns
the service name, version, and an `ok` status. Versioned clients may use
`/api/v1/health`.

## Quick Start

```bash
# 1. Clone the repo
git clone <repo-url>
cd railway-os-platform

# 2. Create your local .env
cp .env.example .env
# Edit .env with your preferred dev passwords

# 3. Validate Docker config
docker compose config

# 4. Start infrastructure
docker compose up -d
docker compose ps
```

## Backend Setup

Windows PowerShell:

```powershell
.\scripts\setup-backend.ps1
```

macOS, Linux, or Git Bash:

```bash
bash scripts/setup-backend.sh
```

These commands create `backend/.venv` and install the pinned backend dependencies.

## Backend Quality Checks

Run formatting verification, linting, and the pytest suite from the repository root:

```powershell
.\scripts\check-backend.ps1
```

```bash
bash scripts/check-backend.sh
```

## Documentation

- [Project Roadmap](docs/project-roadmap.md)
- [Daily Plan (Months 1-4)](docs/first-four-months-daily.md)
- [GitHub Issues & Milestones](docs/day-001-github-issues.md)
- [Environment Variables Guide](docs/environment-guide.md)
- [Day 3 Infrastructure Verification](docs/day-003-infrastructure.md)
- [Day 4 Backend Environment](docs/day-004-backend-environment.md)
- [Architecture](docs/architecture.md)
- [Entity Relationship Diagram](docs/erd.md)
- [Day 15 ERD Design Notes](docs/day-015-erd-design.md)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL 15 |
| Cache / Pub-Sub | Redis 7 |
| Frontend | React + Vite + TypeScript |
| Container | Docker Compose |
| CI | GitHub Actions |
