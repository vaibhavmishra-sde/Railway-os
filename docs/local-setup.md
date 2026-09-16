# Local Setup Guide

Welcome to the RailwayOS backend project. Follow these steps to set up the project locally.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

## Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd railway-os
   ```

2. **Copy Environment Variables**
   ```bash
   cp .env.example .env
   ```

3. **Start the database services**
   ```bash
   docker compose up -d
   ```

4. **Initialize the Python Virtual Environment**
   Using the provided setup script:
   ```bash
   ./scripts/setup-backend.sh
   ```
   Or manually:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   You can verify it works by visiting `http://127.0.0.1:8000/health`.

## Quality Checks

Run tests and linters locally before committing:

```bash
# Run tests
pytest

# Run linter
ruff check .

# Run formatter
ruff format .
```
