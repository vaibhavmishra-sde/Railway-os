# Dated services API contract

The service board calls `GET /api/v1/services` with a required
`service_date=YYYY-MM-DD` query parameter. The response contains the service
identifier, train, route, date, and operational status used by the board.

Clients should preserve the selected date when refreshing results and handle
an empty array as a valid response.
