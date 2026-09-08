# RailwayOS Backend

FastAPI backend for the RailwayOS platform.

## Setup

Run the setup helper from the repository root:

```powershell
.\scripts\setup-backend.ps1
```

On macOS, Linux, or Git Bash:

```bash
bash scripts/setup-backend.sh
```

The scripts create `backend/.venv`, upgrade `pip`, install the pinned runtime dependencies from `requirements.txt`, and install development tooling from `requirements-dev.txt`.

To install only runtime dependencies:

```powershell
.\scripts\setup-backend.ps1 -SkipDev
```

```bash
SKIP_DEV=1 bash scripts/setup-backend.sh
```

## Manual Setup

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements-dev.txt

# macOS/Linux
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt
```

## Directory Structure

```text
backend/
├── app/                  # FastAPI application (Day 5)
│   ├── __init__.py
│   ├── main.py           # App factory + router registration
│   ├── config.py         # pydantic-settings (Day 8)
│   ├── api/              # Route handlers by version
│   │   └── v1/
│   ├── core/             # Shared utilities
│   ├── db/               # SQLAlchemy engine + session (Day 11)
│   ├── models/           # ORM models
│   └── schemas/          # Pydantic request/response schemas
├── alembic/              # Database migrations (Day 12)
├── tests/                # pytest test suite (Day 6)
├── pyproject.toml        # Project metadata + tool config
├── requirements.txt      # Pinned runtime dependencies
├── requirements-dev.txt  # Pinned development dependencies
└── Dockerfile            # Container image (Day 106)
```

## Run the API

From `backend/`, run:

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Check `http://127.0.0.1:8000/health` for a 200 response. The same endpoint is
also exposed at `/api/v1/health` for versioned clients.

## Quality Checks

From the repository root, run the complete backend check suite:

```powershell
.\scripts\check-backend.ps1
```

```bash
bash scripts/check-backend.sh
```

The checks run Ruff formatting verification, Ruff linting, and pytest. Install
the Git hook once after setup to run whitespace, syntax, formatting, and lint
checks before each commit:

```powershell
.\backend\.venv\Scripts\pre-commit install
```

## Current State: Day 006

- [x] Backend dependency manifest is pinned
- [x] Development dependency manifest is pinned
- [x] `backend/.venv` can be created locally and is ignored by Git
- [x] FastAPI app scaffold and `GET /health` endpoint (Day 5)
- [x] Health endpoint and API contract tests (Day 6)
- [x] Ruff formatting/linting and pre-commit checks (Day 6)
- [ ] CI (Day 7)
