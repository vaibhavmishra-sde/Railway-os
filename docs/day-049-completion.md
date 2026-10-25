# Day 49 — Completion

The journey planner now submits the selected route and date to the journey
search endpoint, renders returned services, and reports validation and API
errors inline. Both station fields provide debounced suggestions; pending
lookups are cancelled when the user changes the input.

Verification: `npm.cmd run build` passes from `frontend/`.
