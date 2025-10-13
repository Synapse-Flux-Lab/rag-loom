---
id: requirements
title: Prerequisites & Environment Setup
sidebar_position: 1
---

This guide walks through the prerequisites and environment preparation needed before running RAG Loom locally or in CI.

You can let the project handle everything for you by running `./utilscripts/quick_start.sh setup`. The script installs Python 3.12 , creates a virtual environment, upgrades `pip`, and installs `requirements.txt`. The rest of this page mirrors those steps so you can perform them manually.

## Supported Platforms

- **Operating systems**: macOS 13+, Ubuntu 20.04+, or other modern Linux distributions.
- **Python**: 3.12 is the supported baseline (`quick_start.sh` bootstraps this exact version).
- **Container tooling** (optional): Docker (24+) and Docker Compose (v2) for production parity testing.
- **Git**: Required for cloning and managing the repository.

## Hardware Recommendations

| Scenario | CPU | Memory | Storage |
| --- | --- | --- | --- |
| Local evaluation | 4 cores | 16 GB | 20 GB free |
| Development with Ollama | 8 cores | 32 GB | 50 GB free |
| Production deployment | 8+ cores | 32+ GB | SSD-backed 100 GB free |

> Running local language models with Ollama benefits from Apple Silicon or a modern GPU-enabled Linux host. For lighter development, you can target hosted providers such as OpenAI or Cohere.

## Repository Setup

### 1. Install core prerequisites

Confirm that the following executables are available:

- `python3.12` (or install it)
  - macOS (Homebrew): `brew install python@3.12`
  - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install python3.12 python3.12-venv`
  - Fedora: `sudo dnf install python3.12 python3.12-venv`
- `pip3` (bundled with the installers above; otherwise install `python3-pip` via your package manager)
- `git` (optional for day-to-day work, but required to clone the repo)

Verify the versions:

```bash
python3.12 --version
pip3 --version
git --version
```

### 2. Clone the repository

```bash
git clone https://github.com/Synapse-Flux-Lab/rag-loom.git
cd rag-loom
```

### 3. Create the project virtual environment

Match the automation script by placing the environment in `venvpy312`:

```bash
python3.12 -m venv venvpy312
source venvpy312/bin/activate  # Windows PowerShell: venvpy312\Scripts\Activate.ps1
```

Reusing an existing environment? Just reactivate it with `source venvpy312/bin/activate`.

### 4. Install Python dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

If dependency installation fails, delete the virtual environment (`rm -rf venvpy312`) and recreate it to ensure a clean state.

## Environment Configuration

1. Copy the sample environment file:
   ```bash
   cp docs/static/files/env.example .env
   ```
2. Populate the required secrets and configuration.
3. Review optional toggles for providers, vector stores, and telemetry.

### Essential Settings

| Variable | Purpose | Example |
| --- | --- | --- |
| `LLM_PROVIDER` | Language model backend | `ollama`, `openai`, `cohere` |
| `VECTOR_STORE_TYPE` | Vector storage implementation | `chroma`, `qdrant`, `redis` |
| `OPENAI_API_KEY` | Required when `LLM_PROVIDER=openai` | `sk-...` |
| `COHERE_API_KEY` | Required when `LLM_PROVIDER=cohere` | `...` |
| `QDRANT_URL` / `QDRANT_API_KEY` | Needed when `VECTOR_STORE_TYPE=qdrant` | `http://localhost:6333` / `secret` |

Refer to the inline comments in `.env` for further options.

## Optional Tooling

- **Node.js** (18+): Necessary only when developing documentation locally (`./utilscripts/docs_start.sh`).
- **Make**: Some teams prefer wrapping helper commands in Make targets.
- **Poetry or Pipenv**: Alternative dependency managers if pip is not preferred (update scripts accordingly).

## Next Steps

With prerequisites in place, continue to [Quick Start](./quickstart) to launch the API locally and validate the installation.
