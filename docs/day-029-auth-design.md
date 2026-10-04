# Day 29: Identity and access design

RailwayOS uses application roles to control access to operational workflows.
Authentication is planned for the next implementation days; this document is
the contract that the models, API dependencies, and tests will follow.

## Roles

| Role | Purpose |
| --- | --- |
| `passenger` | Search services and manage the passenger's own bookings. |
| `station_staff` | View station operations and update assigned station workflows. |
| `operations_manager` | Monitor and update network-wide service operations. |
| `admin` | Manage users, roles, and platform configuration. |

Every user has one or more roles. Role names are stable lowercase identifiers;
display labels belong in the API/UI layer.

## Access matrix

| Capability | Passenger | Station staff | Operations manager | Admin |
| --- | ---: | ---: | ---: | ---: |
| Read public stations, routes, and timetables | Yes | Yes | Yes | Yes |
| Manage own profile and bookings | Yes | No | No | No |
| View assigned operational data | No | Yes | Yes | Yes |
| Update station/service operational state | No | Assigned scope | Network-wide | Yes |
| Manage users and roles | No | No | No | Yes |
| Read audit events | Own actions | Assigned scope | Network-wide | Yes |

Authorization must be enforced server-side. The frontend may hide unavailable
actions for usability, but hidden controls are not a security boundary.

## Planned entities

- `User`: identity, normalized email, password hash, active flag, and timestamps.
- `Role`: stable role key and display metadata.
- `UserRole`: unique user/role association.
- `AuditEvent`: actor, action, resource type/id, outcome, request ID, and time.

Audit events must never store passwords, access tokens, or other credentials.
Security-sensitive actions should record both successful and rejected outcomes.

## Authentication decisions

- Passwords are stored only as adaptive password hashes.
- Access tokens are short-lived JWTs; refresh-token rotation is a later task.
- Disabled users are rejected even when presented with an otherwise valid token.
- Missing authentication returns `401`; authenticated users without permission
  receive `403`.

