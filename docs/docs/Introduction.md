---
id: Introduction
title: Introduction
sidebar_position: 1
---

RAG Loom provides a production-quality retrieval-augmented generation (RAG) microservice built on FastAPI. This site covers everything required to evaluate the platform, run it locally, integrate it with external systems, and operate it in production.

## Executive Snapshot

RAG Loom uses power of your proprietary data with the reasoning power of frontier generative AI models, turning static knowledge bases into live, AI-assisted experiences. Within days, business teams move from “we should explore AI” to measurable impact in customer support, research synthesis, and internal enablement.

### What Is Retrieval-Augmented Generation?

Retrieval-augmented generation (RAG) blends two ingredients:

1. **Retrieval** — find trustworthy, business-owned content at the moment of need.  
2. **Generation** — craft concise, conversational answers using large language models that respect your tone and policy guardrails.

The result is an AI copilot that is *grounded* in your company facts, auditable across every answer, and tuned for regulated environments.

### Built for the Models You Already Trust

- 🧠 **OpenAI GPT-4o** — empathetic customer responses with enterprise-grade safety  
- ⚡ **Anthropic Claude 3 Opus** — long-context analysis for legal, research, and policy teams  
- 🌐 **Google Gemini 1.5 Pro** — multimodal synthesis across docs, images, and knowledge graphs  
- 🛠️ **Mistral Large** — European-hosted option for data residency and cost-sensitive deployments

RAG Loom orchestrates these providers behind a consistent API, so business stakeholders can switch between best-of-breed models without disrupting downstream workflows.

### Why It Matters for Business Leaders

- **De-risk AI rollouts** — start with explainable, citation-backed answers instead of black-box chatbots.  
- **Accelerate time to value** — launch pilot use cases in days, not quarters, with governance baked in.  
- **Scale with confidence** — observability dashboards surface trends in adoption, accuracy, and compliance for every release.

Ready to explore tailored roll-out plans? Our partnerships team is one click away on the [Contact RAG Loom Team](./contact-us) page.

## Who This Documentation Serves

- **Builders** who want to stand up RAG Loom locally and explore the API surface.
- **Operators** who deploy and monitor the service in production environments.
- **Integrators** connecting RAG Loom to model providers such as Ollama, OpenAI, or Cohere.
- **Contributors** extending the project or adapting it to bespoke workflows.

## Key Capabilities

- Modular ingestion, retrieval, and generation pipelines with configurable vector stores.
- Support for local and hosted LLM providers (Ollama, OpenAI, Cohere, Hugging Face).
- Production operational tooling, including Dockerised deployment scripts and monitoring.
- Test harnesses and quick-start scripts to accelerate development.

## How to Navigate the Docs

| Section | When to Read | Highlights |
| --- | --- | --- |
| [Getting Started](./getting-started/requirements) | First-time setup | Prerequisites, local bootstrap, project layout |
| [Architecture](./architecture/system-design) | Planning & design reviews | High-level system view and component responsibilities |
| [API](./api/rest-api) | Building client integrations | Endpoint catalogue, payloads, and curl recipes |
| [Operations](./operations/scaling) | Running in production | Scaling strategies, security hardening, troubleshooting guides |
| [Integrations](./integrations/ollama) | Configuring external services | Ollama integration guidance and performance tips |

## Quick Actions

- Copy the environment template: `cp docs/static/files/env.example .env`
- Launch the local stack with the helper script: `./utilscripts/quick_start.sh setup`
- Explore interactive API docs at `http://localhost:8000/docs`
- Run automated tests: `pytest`

## Project Structure

```
rag-loom/
├── app/                      # FastAPI application code
├── docs/                     # Documentation site (Docusaurus)
│   ├── docs/                 # Markdown sources
│   ├── src/                  # Presentation components and styles
│   └── static/files/         # Downloadable assets and samples
├── tests/                    # Automated test suites
├── utilscripts/              # Operational helper scripts
└── Dockerfile                # Containerised deployment
```

Need help fast? Start with [Getting Started](./getting-started/requirements) to prepare your environment, then move on to [Quick Start](./getting-started/quickstart) to launch the service in minutes.
