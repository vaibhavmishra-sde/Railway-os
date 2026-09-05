#!/usr/bin/env bash
# ============================================================
# RailwayOS — scripts/validate-env.sh
# ============================================================
# PURPOSE: Validate that .env exists and that docker compose
#          can resolve all variable references correctly.
#
# USAGE:
#   bash scripts/validate-env.sh
#
# Added: Day 002 — Environment Setup
# ============================================================

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "============================================"
echo " RailwayOS — Environment Validator (Day 002)"
echo "============================================"
echo ""

# ── Step 1: Check .env exists ──────────────────────────────
echo "▶ Checking .env file..."
if [[ ! -f "$ROOT/.env" ]]; then
    echo "  ✗ .env not found!"
    echo "  Run: cp .env.example .env"
    exit 1
fi
echo "  ✓ .env exists"
echo ""

# ── Step 2: Check .env is git-ignored ──────────────────────
echo "▶ Confirming .env is git-ignored..."
if git -C "$ROOT" status --short | grep -q "^?? .env$"; then
    echo "  ✗ .env appears in 'git status' — it is NOT ignored!"
    echo "  Check .gitignore for a '.env' entry."
    exit 1
fi
echo "  ✓ .env is not tracked by git"
echo ""

# ── Step 3: Run docker compose config ──────────────────────
echo "▶ Running 'docker compose config'..."
if docker compose -f "$ROOT/docker-compose.yml" config > /dev/null 2>&1; then
    echo "  ✓ docker compose config succeeded"
else
    echo "  ✗ docker compose config failed!"
    docker compose -f "$ROOT/docker-compose.yml" config
    exit 1
fi
echo ""

# ── Step 4: Check required variables ───────────────────────
echo "▶ Checking required variables in .env..."

REQUIRED_VARS=(
    "POSTGRES_PASSWORD"
    "REDIS_PASSWORD"
    "JWT_SECRET_KEY"
    "DATABASE_URL"
)

source "$ROOT/.env"
MISSING=()

for var in "${REQUIRED_VARS[@]}"; do
    value="${!var:-}"
    if [[ -z "$value" ]]; then
        MISSING+=("$var")
    else
        echo "  ✓ $var is set"
    fi
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
    echo ""
    echo "  ✗ Missing required variables:"
    for var in "${MISSING[@]}"; do
        echo "    - $var"
    done
    exit 1
fi

echo ""
echo "============================================"
echo " ✓ All checks passed! Environment is valid."
echo "============================================"
