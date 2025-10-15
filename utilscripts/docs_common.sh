#!/usr/bin/env bash
# Shared helpers for managing the Docusaurus documentation site.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="${ROOT_DIR}/docs"
PACKAGE_JSON="${DOCS_DIR}/package.json"
STAMP_FILE="${DOCS_DIR}/node_modules/.package-json.sha1"

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

  if [[ -f "${PACKAGE_JSON}" ]]; then
    mkdir -p "$(dirname "${STAMP_FILE}")"
    shasum "${PACKAGE_JSON}" | awk '{print $1}' > "${STAMP_FILE}"
  fi
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

needs_install() {
  if [[ ! -d "${DOCS_DIR}/node_modules" ]]; then
    return 0
  fi

  if [[ ! -f "${STAMP_FILE}" ]]; then
    return 0
  fi

  if [[ ! -f "${PACKAGE_JSON}" ]]; then
    return 1
  fi

  local current_hash stored_hash
  current_hash="$(shasum "${PACKAGE_JSON}" | awk '{print $1}')"
  stored_hash="$(cat "${STAMP_FILE}")"

  [[ "${current_hash}" != "${stored_hash}" ]]
}
