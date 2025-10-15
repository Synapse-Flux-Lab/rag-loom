---
id: roadmap
title: RAG Loom Roadmap
description: Strategic view of RAG Loom's capabilities, current delivery state, and upcoming milestones.
---

## Vision

RAG Loom bundles the components required to stand up a production-grade retrieval augmented generation (RAG) stack. This roadmap outlines what already ships with the platform, clarifies how those capabilities work today, and highlights the near-term enhancements that will round out the experience.

## Roadmap Feature Snapshot

### FastAPI microservice for clean API endpoints
Provides a dedicated service layer with predictable request and response contracts, enabling downstream apps to integrate without custom glue code.

### Vector database integration (pgvector / Milvus / Weaviate)
Delivers low-latency semantic search across indexed knowledge bases, keeping embeddings accessible as content volumes grow.

### RAG orchestration (chunking, embedding, retrieval, answer generation)
Coordinates the ingestion pipeline so every document chunk, embedding, and retrieved context flows into grounded responses.

### Evaluation harness (Ragas / Evals) for quality scoring
Measures answer fidelity, relevance, and coverage so teams can iterate on prompts and data with objective feedback loops.

### Tracing & Observability (Langfuse, structured logging, metrics)
Surfaces traces, logs, and health indicators that make it easy to diagnose regressions and uphold reliability targets.

### Enterprise Guardrails (PII redaction, profanity filter)
Applies policy checks that detect sensitive content, enforce moderation rules, and prevent unsafe material from reaching users.

### Prompt & dataset versioning (Weights & Biases)
Captures prompt templates and corpus snapshots as versioned artifacts, keeping experiments reproducible across environments.

### Deployment ready (Dockerfile, Kubernetes manifests)
Ships container images and orchestration manifests so teams can promote the stack from local testing to production-grade hosting.

## Roadmap Phases

The roadmap is grouped to reflect incremental value delivery. Completed work is marked, and the remaining items show how the stack will evolve.

### Phase 1 — Core Infrastructure (✅ Delivered)

- FastAPI foundation, chunking/embedding pipeline, and base retrieval/generation services shipped with smoke tests.
- Vector store adapters for Chroma, Qdrant, and Redis plus docker-compose infrastructure (`docker-compose.infra.yml`).
- Prometheus metrics, application logging, and `/health` readiness checks in place for day-zero observability.

**Focus:** Harden the service contract and ingestion→retrieval→generation loop so teams can ingest content immediately.

### Phase 2 — Evaluation & Operability Enhancements (🚧 In Progress)

- Expand evaluation coverage using Ragas/OpenAI Evals with templated quality reports.
- Deepen tracing adoption with Langfuse connectors and OpenTelemetry exporters for distributed spans.
- Finalize container publishing workflow and deliver Helm charts/Kubernetes manifests for production rollouts.

**Focus:** Improve feedback loops and operational clarity to shorten the path from experimentation to production tuning.

### Phase 3 — Trust & Governance Controls (🔜 Planned)

- Introduce configurable guardrails for PII redaction, profanity scoring, and escalation hooks.
- Wire prompt and dataset lineage into Weights & Biases to guarantee reproducibility and auditability.
- Document controlled rollout playbooks (blue/green, canary) and automate policy compliance reporting.

**Focus:** Ensure compliance readiness and maintain traceability for enterprise deployments.

## How to Track Progress

- GitHub project board labels (`phase:core`, `phase:ops`, `phase:trust`) map directly to the roadmap phases.
- Docs updates (including this page) land alongside code changes for full change visibility.
- Health and trend monitoring: `/health` surfaces dependency readiness, Prometheus metrics power SLO dashboards, and Langfuse integration milestones will be announced in release notes.

Stay tuned to tagged releases as each phase completes qualification and moves to general availability.
