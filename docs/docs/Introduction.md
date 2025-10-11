id: Introduction
title: Documentation Index
sidebar_position: 1
---

RAG Loom provides a production-quality retrieval-augmented generation (RAG) microservice built on FastAPI. This site covers everything required to evaluate the platform, run it locally, integrate it with external systems, and operate it in production.

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
| [Operations](./operations/deployment) | Deploying or running in production | Deployment automation, monitoring, scaling, troubleshooting |
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
