# Implementation sequence

1. Add password hashing settings and a small service abstraction.
2. Add token encoding and decoding with explicit expiry handling.
3. Add the login schema and endpoint.
4. Add the current-user dependency.
5. Add role dependencies for staff and passenger workflows.
6. Add unit and API tests before wiring protected business endpoints.

Each step should remain independently reviewable and preserve the existing
public network APIs.
