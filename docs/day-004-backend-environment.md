# Day 4 - Backend Python Environment

Date: 2026-09-06

## Goal

Create a reproducible Python environment for the backend and record the dependency manifest needed for FastAPI development.

## Deliverables

- Added pinned backend runtime dependencies in `backend/requirements.txt`.
- Added pinned development tooling in `backend/requirements-dev.txt`.
- Aligned `backend/pyproject.toml` with the pinned dependency versions.
- Added setup helpers for Windows PowerShell and Unix-style shells.
- Kept `backend/.venv` out of version control through the existing `.gitignore` rules.

## Setup Commands

From the repository root on Windows:

```powershell
.\scripts\setup-backend.ps1
```

From macOS, Linux, or Git Bash:

```bash
bash scripts/setup-backend.sh
```

The development install includes the runtime requirements because `requirements-dev.txt` references `requirements.txt`.

## Manual Verification

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt
```

On Windows PowerShell, use:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
```

## Result

Day 4 is complete when a clean checkout can create `backend/.venv` and install all pinned backend dependencies from the repository files.
