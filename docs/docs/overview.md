---
id: overview
title: Platform Overview
sidebar_position: 2
---

This page summarises RAG Loom's capabilities, primary components, and common deployment scenarios. Use it as a high-level orientation before diving into the detailed guides.

## Core Use Cases

| Scenario | Description | Where to Learn More |
| --- | --- | --- |
| Knowledge base search | Ingest private documents and expose semantic search and summarisation | [Quick Start](./getting-started/quickstart), [REST API](./api/rest-api) |
| Production Q&A service | Serve retrieval-augmented responses with observability and scaling | [Scaling](./operations/scaling), [Security](./operations/security) |
| Local experimentation | Run entirely offline with Ollama-backed models | [Ollama Integration](./integrations/ollama) |
| Custom workflow integration | Embed the service within existing platforms or pipelines | [Client Recipes](./api/client-recipes) |

## Feature Highlights

- **Modular pipelines** for ingestion, retrieval, and generation, built on FastAPI.
- **Pluggable vector stores** (Chroma, Qdrant, Redis) and embedding models.
- **Provider abstraction** across Ollama, OpenAI, Cohere, and Hugging Face.
- **Operational tooling** including Docker Compose stacks, monitoring, and helper scripts.
- **Extensibility** through clearly defined service interfaces and configuration options.

## Architecture at a Glance

RAG Loom orchestrates three primary flows:

1. **Ingestion** — Parse documents, generate embeddings, and persist to the configured vector store.
2. **Retrieval** — Perform top-K semantic similarity search over indexed chunks.
3. **Generation** — Assemble prompts from retrieved context and delegate to the chosen LLM provider.

See [System Design Overview](./architecture/system-design) for a detailed diagram and component responsibilities.

## Operational Building Blocks

| Area | Summary |
| --- | --- |
| Deployment | Docker Compose stack with FastAPI, vector stores, optional Ollama, and observability tooling |
| Observability | Prometheus metrics, Grafana dashboards, and health checks |
| Scaling | Horizontal worker scaling, vector store tuning, model selection guidance |
| Security | Authentication hooks, network hardening, and secrets management |

Links to the relevant runbooks are available in the [Operations](./operations/scaling) section.

## Development Workflow

1. Prepare your environment ([Prerequisites](./getting-started/requirements)).
2. Launch locally ([Quick Start](./getting-started/quickstart)).
3. Execute automated tests (`pytest`).
4. Review API schemas at `/docs` and explore example requests in [Client Recipes](./api/client-recipes).
5. Plan production rollout with the [Scaling](./operations/scaling) and [Security](./operations/security) guides.

## Extending the Platform

- Implement new providers by extending the LLM adapter interface in `app/services`.
- Add custom business logic via FastAPI routers under `app/api`.
- Contribute documentation updates by editing the Markdown files in `docs/docs` and using `./utilscripts/docs_start.sh` for live previews.

With the fundamentals in hand, choose the guide that matches your immediate goals—whether that's onboarding, operations, or integration.
