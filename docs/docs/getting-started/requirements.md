---
id: requirements
title: Prerequisites & Environment Setup
sidebar_position: 1
---

This guide walks through the prerequisites and environment preparation needed before running RAG Loom locally or in CI.

## Supported Platforms

- **Operating systems**: macOS 13+, Ubuntu 20.04+, or other modern Linux distributions.
- **Python**: 3.10 or 3.12 (project is validated on 3.12).
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

```bash
git clone https://github.com/Synapse-Flux-Lab/rag-loom.git
cd rag-loom
```

Create an isolated Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

Install the Python dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

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
