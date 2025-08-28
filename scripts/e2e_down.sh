#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)
COMPOSE_BASE="$ROOT_DIR/tests/docker-compose.yml"
COMPOSE_TEST="$ROOT_DIR/tests/docker-compose.test.yml"

echo "[e2e_down] Tearing down stack..."
docker compose -f "$COMPOSE_BASE" -f "$COMPOSE_TEST" down -v
echo "[e2e_down] DONE"


