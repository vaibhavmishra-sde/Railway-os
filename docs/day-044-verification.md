# Day 44 verification

Run from the repository root:

```bash
pytest -q backend/tests
```

The journey-search tests cover case normalization, direct ordered-stop
matching, same-station rejection, unknown stations, reverse journeys, empty
results, and pagination metadata.
