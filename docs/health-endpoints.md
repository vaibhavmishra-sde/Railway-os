# Health endpoints

RailwayOS exposes two operational probes:

| Endpoint | Purpose | Dependencies |
|---|---|---|
| `GET /health` | Confirms that the API process is running. | None |
| `GET /ready` | Confirms that the API can reach its database. | PostgreSQL |

Both endpoints return a small response containing `status`, `service`, and
`version`. Use `/health` for a liveness probe and `/ready` for traffic routing.
