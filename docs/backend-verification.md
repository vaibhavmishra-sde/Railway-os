# Backend verification checklist

Run these commands from the repository root:

```bash
python -m pytest backend/tests
ruff check backend
ruff format --check backend
```

If a check fails, fix the focused module first and rerun the complete suite
before committing. Database-backed tests require the services described in
`docs/local-setup.md`.
