# Day 32 — Login and short-lived access tokens

**Date:** 2026-10-08  
**Area:** Authentication and identity  
**Status:** Planned

## Objective

Implement the first authenticated sign-in path for RailwayOS. A registered,
active user should be able to submit credentials and receive a short-lived
JWT access token without exposing password hashes or other sensitive data.

## Scope

- Add a `POST /api/v1/auth/login` endpoint.
- Normalize the email identifier before lookup.
- Verify credentials through the identity service.
- Issue a signed access token with an explicit expiry.
- Return a generic `401 Unauthorized` response for invalid credentials.
- Keep refresh-token rotation and logout for Day 33.

## Definition of done

- Valid credentials return an access token and expiry metadata.
- Invalid credentials and inactive users receive the same authentication error.
- Tokens contain the user identity and expiry claims.
- Passwords, password hashes, and tokens are not written to logs or responses
  other than the intended login response.
- Focused authentication tests pass.

## Acceptance criteria

- Login returns a short-lived JWT.
- Invalid credentials return 401.


## Implementation checklist

- Add login schema and endpoint.
- Add token creation and expiry handling.

