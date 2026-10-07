# Authentication boundary

The API layer accepts credentials, delegates verification to an authentication
service, and returns a short-lived access token. Route handlers consume the
authenticated principal; they do not query password hashes directly.

The database remains responsible for identity persistence, while token
creation, expiry, and authorization stay in the service layer.
