# Local verification

Before opening the authentication implementation for review, run:

```powershell
cd backend
python -m pytest
ruff check .
```

When the database-backed tests are enabled, start the local services with the
project's Docker Compose instructions and rerun the same commands.
