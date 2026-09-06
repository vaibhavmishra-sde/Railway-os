# RailwayOS

A full-stack railway operations platform built as a portfolio project.

**Current milestone:** Day 4 complete - backend Python environment and dependency manifests are ready. Next up: Day 5 FastAPI application scaffold.

## Progress

| Day | Task | Status |
|-----|------|--------|
| 1 | Read roadmap; create GitHub issues/milestones; verify prerequisites | Done |
| 2 | Copy `.env.example` to `.env`; set dev passwords; validate Docker config | Done |
| 3 | Start PostgreSQL + Redis via Docker; check health, ports, volumes | Done |
| 4 | Create backend Python virtual environment and dependency manifest | Done |
| 5 | Scaffold FastAPI app and local dev server | Next |

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

## Documentation

- [Project Roadmap](docs/project-roadmap.md)
- [Daily Plan (Months 1-4)](docs/first-four-months-daily.md)
- [GitHub Issues & Milestones](docs/day-001-github-issues.md)
- [Environment Variables Guide](docs/environment-guide.md)
- [Day 3 Infrastructure Verification](docs/day-003-infrastructure.md)
- [Day 4 Backend Environment](docs/day-004-backend-environment.md)
- [Architecture](docs/architecture.md)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL 15 |
| Cache / Pub-Sub | Redis 7 |
| Frontend | React + Vite + TypeScript |
| Container | Docker Compose |
| CI | GitHub Actions |
