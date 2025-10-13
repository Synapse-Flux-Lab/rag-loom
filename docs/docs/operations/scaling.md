---
id: scaling
title: Scaling & Performance
sidebar_position: 3
---

RAG Loom scales horizontally and vertically depending on workload characteristics. Use this guidance to size resources and tune performance.

## Horizontal Scaling

Scale the FastAPI service within the docker-compose stack:

```bash
docker compose up -d --scale rag-service=3
```

Behind a load balancer (e.g., Nginx, Traefik), increase worker counts gradually while monitoring latency and error rates. Ensure the vector store can handle the increased concurrency—stateful backends such as Qdrant may require their own scaling strategy.

## Worker Configuration

Gunicorn workers are controlled via environment variables:

| Variable | Description | Recommendation |
| --- | --- | --- |
| `WORKER_PROCESSES` | Number of worker processes | Start with `CPU cores x 2` |
| `MAX_CONCURRENT_REQUESTS` | Concurrent request cap | Tune to protect downstream providers |
| `REQUEST_TIMEOUT` | Timeout per request (seconds) | Increase for long-running generation |

## Vector Store Optimisation

- **Qdrant**: Configure collection parameters (e.g., `hnsw_config`) for recall vs. latency trade-offs; enable snapshots for durability.
- **Redis**: Ensure Redis is compiled with RedisJSON/RedisSearch for vector support; allocate enough memory and persistence policy.
- **Chroma**: Suitable for local development; for production consider migrating to Qdrant or Redis.

## LLM Provider Considerations

| Provider | Notes |
| --- | --- |
| Ollama | Local inference; ensure ample RAM and SSD storage. Set `OLLAMA_NUM_PARALLEL` to control concurrency. |
| OpenAI | Network latency bound; implement retry and backoff. Cache embeddings when possible. |
| Cohere | Similar to OpenAI; monitor rate limits. |
| Hugging Face | Use inference endpoints or host models yourself; plan for GPU utilisation. |

## Performance KPIs

| Metric | Target | Notes |
| --- | --- | --- |
| P95 latency | < 2 seconds for search, < 5 seconds for generate | Monitor separately by endpoint |
| Error rate | < 1% | Break down by provider |
| Document throughput | 200+ documents/hour | Depends on chunking strategy |
| Token usage | Track per provider | Optimise prompt template and chunk size |

## Load Testing

Use tools such as Locust or k6 to simulate traffic:

```bash
locust -f tests/load/locustfile.py --host http://localhost:8000
```

Focus on:

- Mixed workloads (ingest + search + generate).
- Warm and cold cache scenarios.
- Provider failover behaviour.

## Resource Tuning

Docker Compose snippets for resource limits:

```yaml
services:
  rag-service:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
        reservations:
          memory: 1G
  ollama:
    deploy:
      resources:
        limits:
          memory: 32G
```

Adjust based on monitoring data—especially for Ollama, where model size directly impacts RAM requirements.

## Next Steps

After tuning for performance, establish runbooks in [Troubleshooting](./troubleshooting) and review [Security Hardening](./security) before going live.
