# RailwayOS

A full-stack railway operations platform built as a portfolio project.

## Progress

| Day | Task | Status |
|-----|------|--------|
| 1 | Read roadmap; create GitHub issues/milestones; verify prerequisites | ✅ Done |
| 2 | Copy `.env.example` → `.env`; set dev passwords; validate Docker config | ✅ Done |
| 3 | Start PostgreSQL + Redis via Docker; check health, ports, volumes | ⬜ Next |

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

# 4. Start infrastructure (Day 3+)
docker compose up -d
docker compose ps
```

## Documentation

- [Project Roadmap](docs/project-roadmap.md)
- [Daily Plan (Months 1-4)](docs/first-four-months-daily.md)
- [GitHub Issues & Milestones](docs/day-001-github-issues.md)
- [Environment Variables Guide](docs/environment-guide.md)
- [Architecture](docs/architecture.md)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL 15 |
| Cache / Pub-Sub | Redis 7 |
| Frontend | React + Vite + TypeScript |
| Container | Docker Compose |
| CI | GitHub Actions |