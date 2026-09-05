"""
RailwayOS — scripts/validate_env.py
=====================================
Python version of the environment validator for cross-platform use.
Run with: python scripts/validate_env.py

Added: Day 002 — Environment Setup
"""

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent
ENV_FILE = ROOT / ".env"
COMPOSE_FILE = ROOT / "docker-compose.yml"

REQUIRED_VARS = [
    "POSTGRES_PASSWORD",
    "REDIS_PASSWORD",
    "JWT_SECRET_KEY",
    "DATABASE_URL",
    "POSTGRES_DB",
    "POSTGRES_USER",
]

SEPARATOR = "=" * 50


def check(label: str, ok: bool, fix: str = "") -> bool:
    """Print check result."""
    icon = "✓" if ok else "✗"
    print(f"  {icon} {label}")
    if not ok and fix:
        print(f"    Fix: {fix}")
    return ok


def main() -> int:
    print(SEPARATOR)
    print(" RailwayOS — Environment Validator (Day 002)")
    print(SEPARATOR)
    print()

    errors: list[str] = []

    # ── Step 1: .env exists ─────────────────────────────────
    print("▶ Checking .env file...")
    if not check(
        ".env file exists",
        ENV_FILE.exists(),
        fix="cp .env.example .env",
    ):
        errors.append(".env missing")
    print()

    # ── Step 2: Parse .env ──────────────────────────────────
    env_vars: dict[str, str] = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                env_vars[key.strip()] = value.strip()

    # ── Step 3: Required vars ───────────────────────────────
    print("▶ Checking required environment variables...")
    for var in REQUIRED_VARS:
        if not check(
            f"{var} is set",
            bool(env_vars.get(var)),
            fix=f"Add {var}=<value> to .env",
        ):
            errors.append(f"Missing: {var}")
    print()

    # ── Step 4: docker compose config ──────────────────────
    print("▶ Running 'docker compose config'...")
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(COMPOSE_FILE), "config"],
            capture_output=True,
            text=True,
            env={**os.environ, **env_vars},
        )
        if check(
            "docker compose config succeeded",
            result.returncode == 0,
            fix="Run 'docker compose config' manually to see errors",
        ):
            pass
        else:
            print(f"    stderr: {result.stderr[:200]}")
            errors.append("docker compose config failed")
    except FileNotFoundError:
        check("docker compose available", False, fix="Install Docker Desktop")
        errors.append("docker not found")
    print()

    # ── Result ──────────────────────────────────────────────
    print(SEPARATOR)
    if errors:
        print(f" ✗ {len(errors)} check(s) failed:")
        for e in errors:
            print(f"   - {e}")
        print(SEPARATOR)
        return 1

    print(" ✓ All checks passed! Environment is valid.")
    print(SEPARATOR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
