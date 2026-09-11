#!/usr/bin/env bash
set -euo pipefail


repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
backend_dir="$repo_root/backend"
venv_dir="$backend_dir/.venv"
python_bin="${PYTHON_BIN:-python3}"


if ! command -v "$python_bin" >/dev/null 2>&1; then
    echo "Python executable '$python_bin' was not found." >&2
    echo "Set PYTHON_BIN to the Python 3 executable you want to use." >&2
    exit 1
fi


if [[ ! -x "$venv_dir/bin/python" ]]; then
    "$python_bin" -m venv "$venv_dir"
fi


"$venv_dir/bin/python" -m pip install --upgrade pip
"$venv_dir/bin/python" -m pip install -r "$backend_dir/requirements.txt"


if [[ "${SKIP_DEV:-0}" != "1" ]]; then
    "$venv_dir/bin/python" -m pip install -r "$backend_dir/requirements-dev.txt"
fi


echo "Backend virtual environment is ready at $venv_dir"
