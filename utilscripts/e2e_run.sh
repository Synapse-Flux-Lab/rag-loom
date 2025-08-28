#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)
COMPOSE_BASE="$ROOT_DIR/tests/docker-compose.yml"
COMPOSE_TEST="$ROOT_DIR/tests/docker-compose.test.yml"
VENV_DIR="$ROOT_DIR/venvpy312"
BASE_URL_DEFAULT="http://localhost:8000"
SMALL_OLLAMA_MODEL="gemma2:2b"

wait_for() {
  local url=$1
  local name=$2
  local timeout=${3:-240}
  local start=$(date +%s)
  echo -n "[wait] $name: waiting for $url"
  while true; do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo " -> READY"
      break
    fi
    local now=$(date +%s)
    if (( now - start > timeout )); then
      echo " -> TIMEOUT after ${timeout}s" >&2
      exit 1
    fi
    echo -n "."
    sleep 2
  done
}

echo "[e2e] Starting infrastructure via docker compose..."
docker compose -f "$COMPOSE_BASE" -f "$COMPOSE_TEST" up -d qdrant redis ollama

wait_for "http://localhost:6333/readyz" "qdrant" 240
wait_for "http://localhost:11434/api/tags" "ollama" 300

# Pull the model inside the container like utils/ollama-docker.sh
echo "[e2e] Ensuring Ollama model is available (${SMALL_OLLAMA_MODEL})..."
docker exec ollama ollama pull "${SMALL_OLLAMA_MODEL}" || true

echo "[e2e] Preparing Python 3.12 virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
  python3.12 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip >/dev/null 2>&1 || true
pip install -e .
pip install -r "$ROOT_DIR/tests/requirements-test.txt"

echo "[e2e] Launching FastAPI service using utils/quick_start.sh with OLLAMA_MODEL=${SMALL_OLLAMA_MODEL}..."
pushd "$ROOT_DIR" >/dev/null
export OLLAMA_MODEL="${SMALL_OLLAMA_MODEL}"
./utils/quick_start.sh start || true
popd >/dev/null

wait_for "$BASE_URL_DEFAULT/health" "rag-api" 240

export BASE_URL=${BASE_URL:-$BASE_URL_DEFAULT}
echo "[e2e] BASE_URL=$BASE_URL"

echo "[e2e] Running pytest e2e suite..."
pytest -m e2e -q

echo "[e2e] Tests finished. Stopping service and infrastructure..."
pushd "$ROOT_DIR" >/dev/null
./utils/quick_start.sh stop || true
popd >/dev/null

docker compose -f "$COMPOSE_BASE" -f "$COMPOSE_TEST" down -v
echo "[e2e] DONE"


