# Day 003 — Local Infrastructure Startup

**Day:** 3 of 112  
**Date:** 2026-09-05  
**Milestone:** Month 1 — Foundation & Railway Data  
**Week:** Week 1 — Development Foundation

## Task

> Start PostgreSQL and Redis using Docker; check health, ports, and persisted volumes.

**Done when:** Both containers report healthy.

## Verification

`docker compose up -d` completed successfully and created the local Docker network and named volumes:

- `railwayosplatform_postgres_data`
- `railwayosplatform_redis_data`

`docker compose ps` then confirmed both services were healthy:

| Service | Container | Health | Host port |
| --- | --- | --- | --- |
| PostgreSQL 15 | `railwayos_postgres` | healthy | `5432` |
| Redis 7 | `railwayos_redis` | healthy | `6379` |

The named volumes preserve data when containers are stopped or recreated with `docker compose down`. Use `docker compose down -v` only when intentionally resetting local data.

## Commands

```powershell
docker compose up -d
docker compose ps
docker compose logs postgres
docker compose logs redis
```

## Next Day

Day 4 creates the backend Python virtual environment and dependency manifest.
