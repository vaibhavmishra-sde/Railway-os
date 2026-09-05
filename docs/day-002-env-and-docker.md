# Day 002 — Environment Setup & Docker Configuration

**Day:** 2 of 112
**Date:** 2026-09-05
**Milestone:** Month 1 — Foundation & Railway Data
**Week:** Week 1 — Development Foundation

---

## Task

> Copy `.env.example` → `.env`; set safe development passwords; validate Docker configuration.

**Done when:** `docker compose config` succeeds and `.env` is git-ignored.

---

## What Was Done

### 1. Created `.env` from `.env.example`

- Copied `.env.example` to `.env`
- Set all placeholder values to safe development-only passwords
- Confirmed `.env` is listed in `.gitignore` and will never be committed

### 2. Validated `.env` is Git-Ignored

- Ran `git status` → `.env` does **not** appear (correctly untracked/ignored)
- Rule in `.gitignore`: `.env` on line 18 covers this file exactly

### 3. Validated Docker Compose Configuration

- Ran `docker compose config` → printed the fully-resolved YAML with no errors
- All `${VAR:-default}` interpolations were resolved using the values from `.env`
- Services confirmed: `postgres`, `redis`
- Volumes confirmed: `postgres_data`, `redis_data`

### 4. Annotated `docker-compose.yml`

- Updated current state comment from "Phase 1" to "Day 2 / Week 1" for clarity
- Added inline notes on environment variable interpolation

### 5. Created `docs/environment-guide.md`

- Explains every variable in `.env.example`
- Documents how Docker reads the file
- Covers the "why" behind password choices for development

---

## Verification Checklist

- [x] `.env` file exists locally
- [x] `.env` is git-ignored (`git status` does not list it)
- [x] `docker compose config` exits with code 0
- [x] All `${VAR}` references in `docker-compose.yml` resolve correctly
- [x] No hard-coded secrets in any committed file

---

## Commands Run

```bash
# Step 1: Copy template
cp .env.example .env

# Step 2: Confirm git ignores it
git status   # .env must NOT appear here

# Step 3: Validate docker compose reads .env correctly
docker compose config

# Step 4: Check containers are defined
docker compose ps   # shows postgres and redis services
```

---

## Next Day (Day 3)

**Task:** Start PostgreSQL and Redis using Docker; check health, ports, and persisted volumes.
**Done when:** Both containers report healthy (`docker compose ps` shows status `healthy`).

```bash
# Preview for Day 3
docker compose up -d
docker compose ps
docker compose logs postgres
docker compose logs redis
```

---

## Notes & Blockers

- None. All steps completed cleanly.
- `.env` uses `changeme` passwords which are fine for local dev — **never** use in staging/production.
- The `JWT_SECRET_KEY` must be regenerated with `openssl rand -hex 32` before any staging deploy.
