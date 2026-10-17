# Frontend service states

The service board exposes three non-success states deliberately:

- Loading: the selected date is being requested.
- Empty: the API returned no scheduled services for that date.
- Error: the API request failed and the failure message is shown to the user.

This keeps an unavailable service list distinct from a date with no planned
services.
