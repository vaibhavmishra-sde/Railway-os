# RailwayOS — Environment Variables Guide

This document explains every environment variable used by the project.
All variables live in `.env` (local only, git-ignored).
The template lives in `.env.example` (committed, no secrets).

---

## How Docker Reads `.env`

When you run `docker compose up`, Docker Compose automatically reads `.env`
from the same directory as `docker-compose.yml`. Variables are interpolated
into the compose file like this:

```yaml
environment:
  POSTGRES_DB: ${POSTGRES_DB:-railwayos_db}   # uses .env value, or "railwayos_db" if missing
```

The pattern `${VAR:-default}` means:
- Use the value of `VAR` from `.env`
- Fall back to `default` if `VAR` is not set

---

## Variable Reference

### Application

| Variable | Default (dev) | Description |
|----------|--------------|-------------|
| `APP_NAME` | `RailwayOS` | Human-readable app name |
| `APP_VERSION` | `0.1.0` | Current version (matches git tag on release) |
| `APP_ENV` | `development` | Controls feature flags and logging verbosity |
| `DEBUG` | `true` | Enables detailed error messages. **Never `true` in production.** |
| `APP_PORT` | `8000` | FastAPI server port |

### Security — JWT

| Variable | Example | Description |
|----------|---------|-------------|
| `JWT_SECRET_KEY` | `(generated)` | Signs all tokens. Must be ≥32 random bytes. Generate: `openssl rand -hex 32` |
| `JWT_ALGORITHM` | `HS256` | HMAC-SHA256 — fine for single-server deployments |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Short-lived access tokens expire quickly to limit breach window |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh tokens live longer but are one-time-use (rotation) |

> **Security rule:** Never commit `JWT_SECRET_KEY`. If it leaks, all existing tokens can be forged.

### Database — PostgreSQL

| Variable | Dev Value | Description |
|----------|-----------|-------------|
| `POSTGRES_HOST` | `localhost` | Use `postgres` (service name) when running inside Docker network |
| `POSTGRES_PORT` | `5432` | Default PostgreSQL port |
| `POSTGRES_DB` | `railwayos_db` | Database name created on first start |
| `POSTGRES_USER` | `railwayos_user` | Application database user |
| `POSTGRES_PASSWORD` | `changeme` | **Change before staging.** Strong random string in production. |
| `DATABASE_URL` | `postgresql://...` | Full DSN used by SQLAlchemy. Must match the individual vars above. |

### Cache — Redis

| Variable | Dev Value | Description |
|----------|-----------|-------------|
| `REDIS_HOST` | `localhost` | Use `redis` (service name) inside Docker network |
| `REDIS_PORT` | `6379` | Default Redis port |
| `REDIS_PASSWORD` | `changeme` | Redis `requirepass` — must match `docker-compose.yml` command |
| `REDIS_DB` | `0` | Redis logical database index (0 = default) |
| `REDIS_URL` | `redis://:...@localhost:6379/0` | Full URL used by `redis-py` / `aioredis` |

### CORS — Frontend

| Variable | Dev Value | Description |
|----------|-----------|-------------|
| `FRONTEND_URL` | `http://localhost:5173` | Vite dev server origin. Backend allows CORS from this URL only. |

### Seed Data

| Variable | Value | Description |
|----------|-------|-------------|
| `ADMIN_EMAIL` | `admin@railwayos.com` | Created during initial seed. Change password immediately after. |
| `ADMIN_PASSWORD` | `(strong)` | Initial admin password. One-time use during seed. |

---

## Development Setup Steps

```bash
# 1. Copy template
cp .env.example .env

# 2. (Optional) Generate a real JWT secret
python -c "import secrets; print(secrets.token_hex(32))"
# Paste the output into .env as JWT_SECRET_KEY

# 3. Confirm .env is ignored
git status   # .env must NOT appear

# 4. Validate Docker Compose sees all variables
docker compose config   # should print resolved YAML with no errors
```

---

## Environment Differences

| Setting | Development | Staging | Production |
|---------|------------|---------|------------|
| `DEBUG` | `true` | `false` | `false` |
| `APP_ENV` | `development` | `staging` | `production` |
| Passwords | `changeme` | Strong random | Strong random + secret manager |
| `JWT_SECRET_KEY` | Weak OK locally | Generated | Rotated regularly |
| `FRONTEND_URL` | `localhost:5173` | Staging domain | Production domain |

---

## Security Checklist Before Any Deploy

- [ ] All passwords replaced with strong random values
- [ ] `JWT_SECRET_KEY` generated with `openssl rand -hex 32`
- [ ] `DEBUG=false`
- [ ] `APP_ENV=production` (or `staging`)
- [ ] `.env` stored in secrets manager (e.g., Doppler, AWS Secrets Manager, Vault)
- [ ] `.env` **never** committed to Git
