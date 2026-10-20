# Day 47 — Synthetic-network fares

Add deterministic, whole-rupee fares to direct journey search. Fares are
calculated from the route distance and the available coach class, with a
minimum base fare for short synthetic routes. The response exposes one fare
per available class in INR; filtering by `seat_class` still controls which
services match, while the fare map describes all classes on a matching train.

## Rules

- Base fare is `max(50, round(distance_km * 0.9))` INR.
- Class multipliers are General `1.0`, Sleeper `1.35`, Third AC `2.1`,
  Second AC `2.8`, and First AC `4.2`.
- Fares are rounded to whole rupees and are stable for the same route/classes.
