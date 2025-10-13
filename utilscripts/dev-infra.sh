#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.infra.yml"
ENV_TEMPLATE="$ROOT_DIR/env.production"
ENV_FILE="$ROOT_DIR/.env"

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

ensure_prerequisites() {
    if ! command -v docker >/dev/null 2>&1; then
        log_error "Docker is not installed. Please install Docker Desktop or the Docker Engine."
        exit 1
    fi

    if docker info >/dev/null 2>&1; then
        log_info "Docker daemon is available."
    else
        log_error "Docker daemon is not running. Start Docker and retry."
        exit 1
    fi

    if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
        COMPOSE_CMD=("docker" "compose")
    elif command -v docker-compose >/dev/null 2>&1; then
        COMPOSE_CMD=("docker-compose")
    else
        log_error "Neither 'docker compose' nor 'docker-compose' is available."
        exit 1
    fi

    if ! command -v curl >/dev/null 2>&1; then
        log_error "curl is required for readiness checks. Please install curl."
        exit 1
    fi
}

compose() {
    "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" "$@"
}

ensure_compose_file() {
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        log_error "Compose file not found at $COMPOSE_FILE"
        exit 1
    fi
}

ensure_env_file() {
    if [[ ! -f "$ENV_TEMPLATE" ]]; then
        log_error "Template environment file not found at $ENV_TEMPLATE"
        exit 1
    fi

    if [[ ! -f "$ENV_FILE" ]]; then
        log_info "Creating .env from env.production"
        cp "$ENV_TEMPLATE" "$ENV_FILE"
    else
        log_info ".env already exists; ensuring required values."
    fi

    python3 - "$ENV_FILE" <<'PY'
import sys
from pathlib import Path

env_path = Path(sys.argv[1])
if not env_path.exists():
    sys.exit("Missing .env file")

desired = {
    "LLM_PROVIDER": "ollama",
    "OLLAMA_BASE_URL": "http://localhost:11434",
    "OLLAMA_MODEL": "gemma2:2b",
    "VECTOR_STORE_TYPE": "qdrant",
    "QDRANT_URL": "http://localhost:6333",
    "QDRANT_API_KEY": "",
    "SERVICE_PORT": "8000",
    "SERVICE_HOST": "0.0.0.0",
}

lines = env_path.read_text().splitlines()
seen = set()

for idx, raw in enumerate(lines):
    if not raw or raw.lstrip().startswith("#") or "=" not in raw:
        continue
    key, _, _ = raw.partition("=")
    key = key.strip()
    if key in desired:
        value = desired[key]
        lines[idx] = f"{key}={value}"
        seen.add(key)

missing = [k for k in desired if k not in seen]
if missing:
    lines.append("")
    for key in missing:
        lines.append(f"{key}={desired[key]}")

env_path.write_text("\n".join(lines) + "\n")
PY

    log_success ".env configured for Ollama and Qdrant."
}

pull_images() {
    log_info "Pulling container images defined in $(basename "$COMPOSE_FILE")..."
    compose pull
    log_success "Images are up to date."
}

start_stack() {
    log_info "Starting infrastructure stack..."
    compose up -d
    log_success "Containers launched."
}

wait_for_http() {
    local url="$1"
    local name="$2"
    local retries="${3:-30}"
    local delay="${4:-4}"

    log_info "Waiting for ${name} to respond at ${url}..."
    for ((i=1; i<=retries; i++)); do
        if curl -fsS "$url" >/dev/null 2>&1; then
            log_success "${name} is ready."
            return 0
        fi
        sleep "$delay"
    done
    log_error "${name} did not become ready after $((retries * delay)) seconds."
    return 1
}

ensure_ollama_model() {
    local model="gemma2:2b"
    log_info "Ensuring Ollama model ${model} is available..."

    if curl -sfS -X POST http://localhost:11434/api/show \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"${model}\"}" >/dev/null; then
        log_success "${model} already present."
        return 0
    fi

    log_info "Pulling ${model} from Ollama registry (stream=false to block until ready)..."
    local response
    response=$(curl -sS -X POST http://localhost:11434/api/pull \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"${model}\", \"stream\": false}")

    if echo "$response" | grep -q '"status":"success"'; then
        log_success "${model} model downloaded."
    else
        log_error "Model pull failed: $response"
        exit 1
    fi

    if curl -sfS -X POST http://localhost:11434/api/show \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"${model}\"}" >/dev/null; then
        log_success "${model} is available via Ollama API."
    else
        log_error "Unable to verify ${model} presence after pull."
        exit 1
    fi
}

show_status() {
    compose ps
}

show_logs() {
    compose logs -f "$@"
}

stop_stack() {
    log_info "Stopping infrastructure stack..."
    compose down
    log_success "Containers stopped and removed."
}

usage() {
    cat <<EOF
Usage: $(basename "$0") [command]

Commands:
  up        Copy env template, pull images, start containers, and preload models (default)
  down      Stop and remove containers
  restart   Restart the stack (down + up)
  status    Show container status
  logs      Stream container logs (pass additional args for service names)

Examples:
  $(basename "$0")
  $(basename "$0") up
  $(basename "$0") logs qdrant
EOF
}

main() {
    local command="${1:-up}"

    ensure_prerequisites
    ensure_compose_file

    case "$command" in
        up)
            ensure_env_file
            pull_images
            start_stack
            ensure_ollama_model
            log_info "Streaming recent Ollama logs (Ctrl+C to continue)..."
            compose logs --tail=50 ollama || true
            wait_for_http "http://localhost:11434/api/tags" "Ollama API" 40 5
            wait_for_http "http://localhost:6333/health" "Qdrant API"
            log_success "Infrastructure ready. FastAPI service can connect using .env settings."
            ;;
        down)
            stop_stack
            ;;
        restart)
            stop_stack
            "$0" up
            ;;
        status)
            show_status
            ;;
        logs)
            shift || true
            show_logs "$@"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

main "$@"
