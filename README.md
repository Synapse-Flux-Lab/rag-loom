# 📚 RAG Service (Open source Reference Implementation)

## 🔹 Overview

This project is an **open-source reference implementation of a Retrieval-Augmented Generation (RAG) service**.

Unlike most RAG demos, this repo shows how to integrate **document ingestion, vector search, LLM orchestration, evaluation, observability, and guardrails** into a cohesive, deployable microservice.

👉 It’s a **starter kit for AI platform teams**: opinionated, modular, and focused on **enterprise readiness**.

---

## 🔹 Why This Matters

**For professionals:**
Most RAG examples stop at “fetch docs and query an LLM.” This project goes further — adding **eval pipelines, observability, and safety mechanisms** so engineers and product teams can see what *production* looks like.

---

## 🔹 Features

* ✅ **FastAPI microservice** for clean API endpoints
* ✅ **Vector database integration** (pgvector / Milvus / Weaviate)
* ✅ **RAG orchestration** (chunking, embedding, retrieval, answer generation)
* ✅ **Evaluation harness** (Ragas / Evals) for quality scoring
* ✅ **Tracing & Observability** (Langfuse, structured logging, metrics)
* ✅ **Enterprise Guardrails** (PII redaction, profanity filter)
* ✅ **Prompt & dataset versioning** (Weights & Biases)
* ✅ **Deployment ready** (Dockerfile, Kubernetes manifests)

---

## 🔹 Architecture

**Pipeline flow:**
`PDFs → Chunking → Embeddings → Vector DB → Retrieval → LLM → Eval/Guardrails → API Response`

Supporting layers:

* **Observability**: logs, traces, metrics
* **Governance**: SLOs, versioning, risk register

---


## 🔹 Roadmap

* [ ]  Core infra (FastAPI, vector DB, RAG pipeline, basic observability)
* [ ]  Add evals (Ragas/Evals), tracing (Langfuse), Docker/K8s deployment
* [ ]  Add guardrails (PII filter, profanity check), prompt/dataset versioning

---

## 🔹 Contributing

Contributions welcome! Please open issues or submit PRs.

---

## License

This project is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE).

- ✅ Free for noncommercial use: research, personal projects, internal testing, and prototyping
- 💼 Commercial/production use requires a paid license from Synapse Flux Lab

Third-party libraries remain under their original licenses (see [NOTICE](NOTICE)).

For commercial licensing and support, contact us.

