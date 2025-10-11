#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=utilscripts/docs_common.sh
source "${SCRIPT_DIR}/docs_common.sh"

ensure_docs_dir
cd "${DOCS_DIR}"

PACKAGE_MANAGER="$(detect_package_manager)"

if [[ ! -d node_modules ]]; then
  echo "Installing documentation dependencies with ${PACKAGE_MANAGER}..."
  run_install "${PACKAGE_MANAGER}"
fi

echo "Deploying Docusaurus site..."
run_command "${PACKAGE_MANAGER}" deploy

echo "Deployment command completed. Confirm hosting provider settings to finalise publication."
