#!/usr/bin/env bash
# Shared helpers for managing the Docusaurus documentation site.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="${ROOT_DIR}/docs"

ensure_docs_dir() {
  if [[ ! -d "${DOCS_DIR}" ]]; then
    echo "Docs directory not found at ${DOCS_DIR}" >&2
    exit 1
  fi
}

detect_package_manager() {
  if command -v pnpm >/dev/null 2>&1 && [[ -f "${DOCS_DIR}/pnpm-lock.yaml" ]]; then
    echo "pnpm"
  elif command -v yarn >/dev/null 2>&1 && [[ -f "${DOCS_DIR}/yarn.lock" ]]; then
    echo "yarn"
  else
    echo "npm"
  fi
}

run_install() {
  local pm="$1"
  case "${pm}" in
    pnpm) pnpm install ;;
    yarn) yarn install ;;
    npm) npm install ;;
    *)
      echo "Unsupported package manager: ${pm}" >&2
      exit 1
      ;;
  esac
}

run_command() {
  local pm="$1"
  shift
  case "${pm}" in
    pnpm) pnpm "$@" ;;
    yarn) yarn "$@" ;;
    npm) npm run "$@" ;;
    *)
      echo "Unsupported package manager: ${pm}" >&2
      exit 1
      ;;
  esac
}
