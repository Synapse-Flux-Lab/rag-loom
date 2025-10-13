---
id: troubleshooting
title: Troubleshooting Runbooks
sidebar_position: 5
---

This section catalogues common operational issues and recovery steps for RAG Loom deployments.

## Service Does Not Start

1. Inspect logs:
   ```bash
   docker compose logs -f rag-service
   ```
2. Verify dependencies:
   - Vector store container is running.
   - LLM provider credentials are valid.
3. Restart the service:
   ```bash
   docker compose restart rag-service
   ```

## Health Check Fails

- Confirm the service port (default `8000`) is free: `lsof -i:8000`.
- Validate `.env` configuration (missing credentials often surface here).
- For provider outages, switch to a fallback provider or reduce load until the primary recovers.

## Ollama Errors

```bash
# Check running models
ollama list

# Restart the service
brew services restart ollama  # macOS
# or
docker compose restart ollama
```

If downloads fail, remove and re-pull the model:

```bash
ollama rm mistral:7b
ollama pull mistral:7b
```

## High Memory Usage

- Monitor container usage: `docker stats`.
- Reduce Ollama model size (`OLLAMA_MODEL=mistral:7b`).
- Tune chunk sizes in ingestion to minimise embedding footprint.

## Port Conflicts

```bash
lsof -i:8000
lsof -i:6333
lsof -i:6379
sudo lsof -ti:8000 | xargs sudo kill -9
```

Adjust exposed ports in `docker-compose.yml` if conflicts persist.

## Slow Responses

- Review dashboards for latency spikes (see [Monitoring](./monitoring)).
- Increase worker processes (`WORKER_PROCESSES`) or scale horizontally.
- Check vector store load; upgrade storage or increase cache size.
- Analyse LLM provider throughput—consider queueing or request shaping.

## Resetting the Stack

For full redeployments:

```bash
docker compose down -v
./start_production.sh
```

Rebuild images after major code changes:

```bash
docker compose build --no-cache rag-service
docker compose up -d rag-service
```

## Support Checkpoints

- **Logs**: `docker compose logs -f`
- **Metrics**: Grafana dashboards and Prometheus alerts
- **Tests**: `pytest test_service.py`
- **Backups**: Ensure recent snapshots exist before invasive changes

Combine this runbook with your organisation’s incident management playbook for complete coverage.
