---
id: deployment
title: Production Deployment
sidebar_position: 1
draft: true
---

RAG Loom ships with a Docker-based production stack orchestrated via `start_production.sh`. This document explains how to configure, launch, and validate that stack.

## Prerequisites

- Docker and Docker Compose v2 installed.
- Access to the required model providers (Ollama pull permissions, API keys for hosted providers).
- At least 16 GB RAM and 50 GB of free disk space on the host.

## Configuration

1. Copy the production template:
   ```bash
   cp env.production .env
   ```
2. Update credentials, provider choices, and resource settings.
3. Confirm that referenced volumes (e.g., for Qdrant, Redis, Ollama) exist or will be created automatically.

Key environment variables:

| Variable | Description |
| --- | --- |
| `LLM_PROVIDER` | `ollama`, `openai`, `cohere`, or `huggingface` |
| `VECTOR_STORE_TYPE` | `qdrant`, `redis`, or `chroma` |
| `WORKER_PROCESSES` | Gunicorn worker count (set per CPU core) |
| `ENABLE_METRICS` | Toggles Prometheus metrics export |
| `ENABLE_AUTH` | Enables authentication middleware (implement custom handler) |

## Starting the Stack

```bash
chmod +x start_production.sh         # one-time setup
./start_production.sh
```

The script launches the docker-compose topology, including:

- `rag-service`: FastAPI application served via Gunicorn.
- `qdrant` (default): Vector database.
- `redis`: Caching layer (optional).
- `ollama`: Local LLM runtime (optional, depending on provider).
- `prometheus` and `grafana`: Observability stack.

Verify the deployment:

```bash
docker compose ps
curl http://localhost:8000/health
```

## Updating the Deployment

When pushing new application code:

```bash
docker compose build rag-service
docker compose up -d rag-service
```

For dependency changes, rebuild the image with `--no-cache`.

## Rolling Back

1. Scale down the latest workers:
   ```bash
   docker compose up -d --scale rag-service=1
   ```
2. Restore the previous image tag or container snapshot.
3. Validate with smoke tests before increasing capacity.

## Backups

- **Qdrant snapshots**:
  ```bash
  docker compose exec qdrant qdrant snapshot create
  ```
- **Redis data**:
  ```bash
  docker compose exec redis redis-cli BGSAVE
  ```
- **Ollama models**:
  ```bash
  cp -r ~/.ollama ./backups/ollama-$(date +%Y%m%d)
  ```

## Post-Deployment Checklist

- Health endpoint returns `status: healthy`.
- Grafana dashboards display metrics for all services.
- Alerts (if configured) are enabled and confirmed.
- Smoke tests (`pytest test_service.py`) pass against the deployed instance.

Proceed to [Troubleshooting](./troubleshooting) for operational runbooks and verify your Prometheus/Grafana stack is collecting metrics from the service.
