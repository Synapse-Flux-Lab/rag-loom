#!/usr/bin/env bash

# RAG Loom - Test Environment Bootstrap
# Creates a Python 3.12 virtual environment and installs runtime + test dependencies.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

DEFAULT_VENV_DIR="${REPO_ROOT}/venv-tests"
PYTHON_REQUIRED_MAJOR=3
PYTHON_REQUIRED_MINOR=12

VENV_DIR="${DEFAULT_VENV_DIR}"
PYTHON_CMD=""
TORCH_INDEX_URL=""

usage() {
  cat <<'EOF'
Usage: test_env_setup.sh [options]

Options:
  --venv <path>         Custom virtual environment directory (default: ./venv-tests)
  --python <binary>     Explicit Python interpreter to use (must be 3.12.x)
  --torch-index <url>   Optional index URL for installing torch CPU wheels
  -h, --help            Show this help message

Examples:
  ./utilscripts/test_env_setup.sh
  ./utilscripts/test_env_setup.sh --venv .venv --torch-index https://download.pytorch.org/whl/cpu
EOF
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

abs_path() {
  local input_path="$1"
  if [[ "${input_path}" = /* ]]; then
    printf '%s\n' "${input_path}"
  else
    local dir part
    dir="$(cd "$(dirname "${input_path}")" && pwd)"
    part="$(basename "${input_path}")"
    printf '%s/%s\n' "${dir}" "${part}"
  fi
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --venv)
        [[ $# -ge 2 ]] || { echo "Missing value for --venv" >&2; exit 1; }
        VENV_DIR="$(abs_path "$2")"
        shift 2
        ;;
      --python)
        [[ $# -ge 2 ]] || { echo "Missing value for --python" >&2; exit 1; }
        PYTHON_CMD="$2"
        shift 2
        ;;
      --torch-index)
        [[ $# -ge 2 ]] || { echo "Missing value for --torch-index" >&2; exit 1; }
        TORCH_INDEX_URL="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown argument: $1" >&2
        usage
        exit 1
        ;;
    esac
  done
}

select_python() {
  if [[ -n "${PYTHON_CMD}" ]]; then
    if ! command_exists "${PYTHON_CMD}"; then
      echo "❌ Requested Python interpreter '${PYTHON_CMD}' not found." >&2
      exit 1
    fi
    return
  fi

  for candidate in python3.12 python3 python; do
    if command_exists "${candidate}"; then
      local major minor
      major="$("${candidate}" -c 'import sys; print(sys.version_info.major)')"
      minor="$("${candidate}" -c 'import sys; print(sys.version_info.minor)')"
      if [[ "${major}" == "${PYTHON_REQUIRED_MAJOR}" && "${minor}" == "${PYTHON_REQUIRED_MINOR}" ]]; then
        PYTHON_CMD="${candidate}"
        return
      fi
    fi
  done

  echo "❌ Unable to find Python ${PYTHON_REQUIRED_MAJOR}.${PYTHON_REQUIRED_MINOR}. Please install it (e.g. via pyenv, asdf, or your OS package manager)." >&2
  exit 1
}

verify_python_version() {
  local version
  version="$("${PYTHON_CMD}" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"
  local major minor _ IFS='.'
  read -r major minor _ <<< "${version}"
  if [[ "${major}" != "${PYTHON_REQUIRED_MAJOR}" || "${minor}" != "${PYTHON_REQUIRED_MINOR}" ]]; then
    echo "❌ Python interpreter '${PYTHON_CMD}' is version ${version}. Expected ${PYTHON_REQUIRED_MAJOR}.${PYTHON_REQUIRED_MINOR}.x." >&2
    exit 1
  fi
}

create_virtualenv() {
  if [[ -d "${VENV_DIR}" ]]; then
    echo "ℹ️  Reusing existing virtual environment at ${VENV_DIR}"
  else
    echo "📦 Creating virtual environment at ${VENV_DIR}"
    "${PYTHON_CMD}" -m venv "${VENV_DIR}"
  fi
}

activate_virtualenv() {
  if [[ ! -f "${VENV_DIR}/bin/activate" ]]; then
    echo "❌ Virtual environment at ${VENV_DIR} appears corrupted (missing bin/activate)." >&2
    echo "   Remove the directory and re-run this script." >&2
    exit 1
  fi
  # shellcheck disable=SC1090
  source "${VENV_DIR}/bin/activate"
}

install_dependencies() {
  echo "⬆️  Upgrading pip/setuptools/wheel"
  python -m pip install --upgrade pip setuptools wheel

  if [[ -n "${TORCH_INDEX_URL}" ]]; then
    echo "📥 Installing torch from ${TORCH_INDEX_URL}"
    python -m pip install "torch>=2.5.0,<2.6.0" --index-url "${TORCH_INDEX_URL}"
  fi

  echo "📥 Installing application requirements"
  python -m pip install -r "${REPO_ROOT}/requirements.txt"

  echo "📥 Installing test requirements"
  python -m pip install -r "${REPO_ROOT}/tests/requirements-test.txt"
}

main() {
  parse_args "$@"
  select_python
  verify_python_version
  create_virtualenv
  activate_virtualenv
  install_dependencies

  echo
  echo "✅ Test environment ready."
  echo "   To activate later: source \"${VENV_DIR}/bin/activate\""
  echo
}

main "$@"
