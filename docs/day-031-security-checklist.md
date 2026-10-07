# Security checklist

- Never log passwords, password hashes, tokens, or authorization headers.
- Use a slow, memory-hard password hashing configuration.
- Keep access tokens short-lived and validate expiry on every request.
- Return generic authentication failures.
- Assign roles from persisted data, not from client-provided claims.
- Add audit events for successful and failed authentication attempts.
