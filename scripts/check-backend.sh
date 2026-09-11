#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
backend_dir="$repo_root/backend"
python_bin="$backend_dir/.venv/bin/python"


if [[ ! -x "$python_bin" ]]; then
    echo "Backend virtual environment not found. Run bash scripts/setup-backend.sh first." >&2
    exit 1
fi

cd "$backend_dir"
"$python_bin" -m ruff format --check .
"$python_bin" -m ruff check .
"$python_bin" -m pytest
