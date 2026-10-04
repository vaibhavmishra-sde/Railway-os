# Day 30: User and role model implementation plan

This plan turns the Day 29 access contract into database work while keeping
authorization auditable and safe to evolve.

## Model constraints

- `users.email` is normalized to lowercase before uniqueness validation.
- `users.password_hash` is required and is never exposed by response schemas.
- `users.is_active` defaults to `true`; disabled users cannot authenticate.
- `roles.key` is a unique lowercase identifier from the approved role list.
- `user_roles` has a unique `(user_id, role_id)` pair.
- Deleting a user removes role assignments but preserves audit events.
- Audit events retain actor identity as nullable so historical records survive
  account removal or service-level actions.

## Migration and seed order

1. Create `users` and `roles` tables.
2. Create the `user_roles` association table and its uniqueness constraint.
3. Create `audit_events` with indexes for actor, resource, and timestamp.
4. Seed the four approved roles from the Day 29 contract idempotently.
5. Add model and API tests for normalization, uniqueness, and role assignment.

The migration must be reversible. Role seeding belongs in an application seed
step rather than a migration so environments can safely re-run it.

## Acceptance checks

- A repeated seed creates no duplicate roles.
- Duplicate emails and role keys are rejected at the database boundary.
- A user can have several roles but cannot receive the same role twice.
- Password hashes and audit metadata are excluded from public user responses.
- Tests use the isolated database fixture and do not require external services.

