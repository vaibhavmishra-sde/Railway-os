# RailwayOS Core Schema Reference

This reference documents the Month 1 railway entities implemented through Day 21.
All identifiers are UUID strings. Times are timezone-aware UTC values unless noted.

| Table | Purpose | Important constraints |
| --- | --- | --- |
| `stations` | Passenger and operational locations | Unique station code |
| `trains` | Physical trainsets | Unique train number |
| `coaches` | Carriages attached to a train | Unique `(train_id, coach_number)` |
| `seats` | Sellable positions inside coaches | Unique `(coach_id, seat_number)`; cascade on coach deletion |
| `routes` | Ordered network routes | Unique route code |
| `route_stops` | Stations and distances on a route | Unique `(route_id, stop_sequence)` and station |
| `train_services` | A train operating on a date | Unique `(train_id, service_date)` |
| `service_stops` | Timetable stops for a service | Unique `(service_id, stop_sequence)` |

## Seat rules

`seat_class` belongs to the coach, while `berth_type` belongs to the individual
seat. A coach may contain multiple seats with different berth types, but a seat
number may occur only once within that coach. Deleting a coach cascades to its
seats; deleting a train cascades through its coaches and seats.

The database migration is the authoritative enforcement layer. API validation
should provide friendly errors before persistence, while the unique constraints
remain necessary for concurrent writes.
