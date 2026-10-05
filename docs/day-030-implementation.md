# Day 30: Identity model implementation

The authentication foundation is now represented in the database layer.

## Delivered

- `users` stores normalized identity data and password hashes only.
- `roles` stores stable authorization keys.
- `user_roles` prevents duplicate assignments.
- `audit_events` keeps security actions queryable after a user is removed.
- The migration is reversible and can be applied independently of application seed data.

## Next milestone

Add password hashing, login/token endpoints, and server-side role dependencies. Public user responses must never expose `password_hash` or audit metadata.
