# Protected API contract

The login endpoint is `POST /api/v1/auth/login`.

Successful responses return an access token and its expiry metadata. Invalid
credentials return a consistent `401 Unauthorized` response. Missing tokens
also return `401`; valid tokens without the required role return `403`.

The authenticated identity endpoint is `GET /api/v1/auth/me` and requires an
`Authorization: Bearer <access_token>` header. It returns the user's `id`,
`email`, and `is_active` fields. Password hashes and token values are never
included in this response.

The contract keeps authentication failures distinct from malformed request
bodies while avoiding account enumeration.
