---
id: monitoring
title: Monitoring & Observability
sidebar_position: 2
draft: true
---

The production stack includes Prometheus for metrics collection and Grafana for visualisation. This guide explains how to leverage both and extend them for your environment.

## Prometheus

- **URL**: `http://localhost:9090`
- **Default retention**: 200 hours (configure in `docker-compose.yml`).
- **Scrape targets**:
  - `rag-service`: Application metrics (request rate, latency, error counts).
  - `qdrant` / `redis`: Vector and cache health.
  - `ollama`: LLM runtime status (when enabled).

### Key Metrics

| Metric | Description |
| --- | --- |
| `http_server_requests_seconds_*` | Response latency for API endpoints |
| `rag_ingestion_documents_total` | Number of ingested documents |
| `rag_generation_failures_total` | Failed LLM generation attempts |
| `rag_vector_search_duration_seconds_*` | Latency of vector searches |

Configure alerting rules in `prometheus.yml` to integrate with PagerDuty, Opsgenie, or Slack.

## Grafana

- **URL**: `http://localhost:3000`
- **Default credentials**: `admin/admin` (change on first login).
- **Dashboards**: Import the provided JSON dashboards from `docs/static/files/grafana/` (if present) or create custom panels.

Suggested dashboards:

- **Service overview**: Request rates, latencies, error distribution.
- **Vector store health**: Qdrant or Redis resource consumption and query latencies.
- **LLM performance**: Generation duration, token counts, provider error rates.
- **System health**: CPU, memory, disk utilisation of host and containers.

## Logs

Application logs default to structured JSON. Tail via Docker:

```bash
docker compose logs -f rag-service
```

Or follow the quick-start script helper:

```bash
./utilscripts/quick_start.sh logs
```

Ship logs to your central platform (e.g., Loki, ELK) by adding sidecar exporters or updating the logging configuration in `app/core/logging.py`.

## Health Checks

- **FastAPI**: `GET /health` verifies vector store/LLM connectivity.
- **Qdrant**: `GET /health` on the Qdrant container.
- **Ollama**: `GET http://localhost:11434/api/generate` with a lightweight prompt.

Automate checks with your orchestrator (Kubernetes, Nomad) or infrastructure monitoring.

## Alerting Recommendations

| Condition | Suggested Threshold | Action |
| --- | --- | --- |
| High error rate | > 2% of requests failing over 5 minutes | Page operator, check logs |
| Elevated latency | P95 > 5 seconds for search/generate | Investigate vector store or LLM provider |
| Vector store unresponsive | Health check failure | Failover to backup or restart service |
| LLM provider errors | Consecutive failures > 3 | Switch to fallback provider |

## Next Steps

- Extend dashboards with business-specific metrics.
- Integrate tracing (OpenTelemetry) if you require end-to-end request visibility.
- Continue with [Scaling & Performance](./scaling) to plan capacity improvements.
