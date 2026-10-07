# Protected API contract

The planned login endpoint is `POST /api/v1/auth/login`.

Successful responses return an access token and its expiry metadata. Invalid
credentials return a consistent `401 Unauthorized` response. Missing tokens
also return `401`; valid tokens without the required role return `403`.

The contract keeps authentication failures distinct from malformed request
bodies while avoiding account enumeration.
