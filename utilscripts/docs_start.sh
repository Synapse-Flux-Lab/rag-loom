#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=utilscripts/docs_common.sh
source "${SCRIPT_DIR}/docs_common.sh"

ensure_docs_dir
cd "${DOCS_DIR}"

PACKAGE_MANAGER="$(detect_package_manager)"

if needs_install; then
  echo "Installing documentation dependencies with ${PACKAGE_MANAGER}..."
  run_install "${PACKAGE_MANAGER}"
fi

echo "Starting Docusaurus dev server (press Ctrl+C to stop)..."
case "${PACKAGE_MANAGER}" in
  pnpm) pnpm start "$@" ;;
  yarn) yarn start "$@" ;;
  npm) npm run start -- "$@" ;;
esac
