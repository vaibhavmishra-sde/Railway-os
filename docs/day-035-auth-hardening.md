# Day 35 — Authentication hardening

## Objective

Protect login from repeated attempts while documenting the authentication
contract and keeping both successful and negative paths covered by tests.

## Authentication flow

1. `POST /api/v1/auth/register` creates an active user with a password hash.
2. `POST /api/v1/auth/login` accepts an email and password and returns a
   short-lived bearer token.
3. Clients send that token as `Authorization: Bearer <token>`.
4. `GET /api/v1/auth/me` resolves the active user without returning password
   data.
5. Administrative mutations require an allowed role and return `403` for an
   authenticated user with insufficient permissions.

Invalid credentials return `401` without revealing whether an account exists.
After five attempts for the same client and normalized email within 60 seconds,
login returns `429` and a `Retry-After` header.

## Verification

Run the backend suite from the repository root:

```powershell
python -m pytest backend/tests -q
```

The limiter is intentionally process-local for the current development
deployment. A multi-instance deployment should move these counters to Redis.
