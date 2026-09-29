# Day 24: Synthetic timetable seed

RailwayOS now has a repeatable local seed for the complete synthetic timetable.
It creates 12 stations, 3 routes, 5 trains, 15 coaches, 90 seats, 5 dated
services, and 58 ordered service stops.

Run it from the backend directory after applying migrations:

```powershell
.\.venv\Scripts\python -m scripts.seed_network
```

The seed uses stable station, route, and train catalog identifiers. Running it
again does not create duplicate rows, so it is safe for local demo resets and
development startup scripts.

See [Timetable API usage](day-024-api-usage.md) for the read-only service and
stop endpoints.
