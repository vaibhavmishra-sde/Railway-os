# Day 34 — Add role guards for administrative operations

**Status:** Complete

## Objective

Require an authenticated administrative or operations role before mutating
dated train services and timetable stops.

## Implementation

- Added a reusable `require_roles` dependency next to the bearer-user resolver.
- Protected service, route, train, timetable-stop, and coach creation for
  `admin` and `operations_manager` users.
- Added a generic HTTP 403 response for authenticated users without an allowed
  role.

## Verification

Focused authentication tests cover missing-role rejection and the allowed-role
path.
