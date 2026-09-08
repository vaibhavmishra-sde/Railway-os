# RailwayOS — Scripts

Helper scripts for development tasks. All scripts are safe to run locally.

## Available Scripts

| Script | Language | Purpose | Added |
|--------|----------|---------|-------|
| `validate-env.sh` | Bash | Validate `.env` and `docker compose config` | Day 002 |
| `validate_env.py` | Python | Cross-platform version of the above | Day 002 |
| `check-backend.ps1` | PowerShell | Run backend formatting, linting, and tests | Day 006 |
| `check-backend.sh` | Bash | Run backend formatting, linting, and tests | Day 006 |

## Usage

```bash
# Bash (Linux/macOS/WSL)
bash scripts/validate-env.sh

# Python (Windows/Linux/macOS)
python scripts/validate_env.py

# Backend checks (Windows PowerShell)
.\scripts\check-backend.ps1

# Backend checks (Linux/macOS/WSL)
bash scripts/check-backend.sh
```

## Coming Soon

| Script | Purpose | Planned Day |
|--------|---------|-------------|
| `seed.py` | Seed development database | Day 23 |
| `generate-pnr.py` | PNR collision-safe generator demo | Day 60 |
| `simulate-location.py` | Emit fake train location updates | Day 90 |
| `demo-data.py` | Reset DB to clean demo state | Day 111 |
