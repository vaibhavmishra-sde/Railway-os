# RailwayOS Backend

FastAPI backend for the RailwayOS platform.

## Setup (Day 2 — after Day 4 adds venv)

```bash
# From repo root
cp .env.example .env   # Day 2
# Day 4: python -m venv .venv && pip install -r requirements.txt
# Day 5: uvicorn app.main:app --reload
```

## Directory Structure (evolves over Month 1)

```
backend/
├── app/                  # FastAPI application (Day 5)
│   ├── __init__.py
│   ├── main.py           # App factory + router registration
│   ├── config.py         # pydantic-settings (Day 8)
│   ├── api/              # Route handlers by version
│   │   └── v1/
│   ├── core/             # Shared utilities (logging, errors)
│   ├── db/               # SQLAlchemy engine + session (Day 11)
│   ├── models/           # ORM models (Week 3)
│   └── schemas/          # Pydantic request/response schemas
├── alembic/              # Database migrations (Day 12)
├── tests/                # pytest test suite (Day 6)
├── pyproject.toml        # Project metadata + tool config
├── requirements.txt      # Pinned dependencies (Day 4)
└── Dockerfile            # Container image (Day 106)
```

## Current State: Day 002

- [x] `.env` template present and documented
- [ ] Python venv (Day 4)
- [ ] FastAPI app (Day 5)
- [ ] Tests (Day 6)
- [ ] CI (Day 7)
