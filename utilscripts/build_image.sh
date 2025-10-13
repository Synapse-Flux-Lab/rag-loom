#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKERFILE="$ROOT_DIR/Dockerfile"

IMAGE_NAME="rag-loom"
IMAGE_TAG="local"
PUSH_IMAGE=false

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Build a lightweight local Docker image for the RAG Loom service.

Options:
  -n, --name NAME       Image name (default: ${IMAGE_NAME})
  -t, --tag TAG         Image tag (default: ${IMAGE_TAG})
  -p, --push            Push the image after building
  -h, --help            Show this help message and exit

Examples:
  $(basename "$0")
  $(basename "$0") --tag dev
  $(basename "$0") --name my-registry/rag-loom --tag latest --push
EOF
}

log() {
    local level="$1"; shift
    printf "[%s] %s\n" "$level" "$*"
}

ensure_prerequisites() {
    if ! command -v docker >/dev/null 2>&1; then
        log ERROR "Docker is not installed. Please install Docker Desktop or Docker Engine."
        exit 1
    fi

    if ! docker info >/dev/null 2>&1; then
        log ERROR "Docker daemon is not running. Start Docker and retry."
        exit 1
    fi

    if [[ ! -f "$DOCKERFILE" ]]; then
        log ERROR "Dockerfile not found at $DOCKERFILE"
        exit 1
    fi
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -n|--name)
                IMAGE_NAME="$2"
                shift 2
                ;;
            -t|--tag)
                IMAGE_TAG="$2"
                shift 2
                ;;
            -p|--push)
                PUSH_IMAGE=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log ERROR "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
}

build_image() {
    local full_tag="${IMAGE_NAME}:${IMAGE_TAG}"

    log INFO "Building image ${full_tag}..."
    docker build \
        --file "$DOCKERFILE" \
        --tag "$full_tag" \
        --pull \
        "$ROOT_DIR"

    log INFO "Image built successfully."
    docker image inspect "$full_tag" --format='{{json .Size}}' \
        | awk '{ printf "[INFO] Image size: %.2f MB\n", $1 / (1024*1024) }'

    if [[ "$PUSH_IMAGE" == true ]]; then
        log INFO "Pushing image ${full_tag}..."
        docker push "$full_tag"
        log INFO "Image pushed."
    fi
}

parse_args "$@"
ensure_prerequisites
build_image
