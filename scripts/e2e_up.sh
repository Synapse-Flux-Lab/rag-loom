#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)
COMPOSE_BASE="$ROOT_DIR/tests/docker-compose.yml"
COMPOSE_TEST="$ROOT_DIR/tests/docker-compose.test.yml"

echo "[e2e_up] Bringing up stack..."
docker compose -f "$COMPOSE_BASE" -f "$COMPOSE_TEST" up -d

wait_for() {
  local url=$1
  local name=$2
  local timeout=${3:-180}
  local start=$(date +%s)
  echo -n "[wait] $name: waiting for $url"
  while true; do
    if curl -fsS "$url" > /dev/null 2>&1; then
      echo " -> READY"
      break
    fi
    now=$(date +%s)
    if (( now - start > timeout )); then
      echo " -> TIMEOUT after ${timeout}s" >&2
      exit 1
    fi
    echo -n "."
    sleep 2
  done
}

wait_for "http://localhost:6333/readyz" "qdrant" 240
wait_for "http://localhost:11434/api/tags" "ollama" 300
wait_for "http://localhost:8000/health" "rag-api" 240

export BASE_URL=${BASE_URL:-http://localhost:8000}
echo "[e2e_up] BASE_URL=$BASE_URL"
echo "[e2e_up] READY"


