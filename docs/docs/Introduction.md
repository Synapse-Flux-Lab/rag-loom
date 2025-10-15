---
id: Introduction
title: Introduction
sidebar_position: 1
---

RAG Loom provides a production-quality retrieval-augmented generation (RAG) microservice built on FastAPI. This site covers everything required to evaluate the platform, run it locally, integrate it with external systems, and operate it in production.



<div class="executive-card">
  <div class="executive-card__intro">
  ## Executive Snapshot
    <p>
      RAG Loom allows to use your proprietary data with frontier generative AI, turning static knowledge bases into live, AI-assisted experiences. Within days, business teams move from “we should explore AI” to measurable impact in customer support, research synthesis, and internal enablement.
    </p>
  </div>
  <div class="executive-card__grid">
    <div class="executive-card__section">
      <h3>What Is Retrieval-Augmented Generation?</h3>
      <ol class="executive-card__list">
        <li><strong>Retrieval</strong> — surface the right internal answer in milliseconds, straight from your knowledge base.</li>
        <li><strong>Generation</strong> — blend that source material into clear, on-brand narratives for customers and teams.</li>
      </ol>
      <p class="executive-card__note">
        The result is an AI copilot that stays grounded in policy-approved facts and gives stakeholders instant confidence.
      </p>
    </div>
    <div class="executive-card__section">
      <h3>Built for the Models You Already Trust</h3>
      <ul class="executive-card__models">
        <li><span class="executive-card__emoji"></span><span class="executive-card__model-text"><strong>OpenAI GPT</strong> </span></li>
        <li><span class="executive-card__emoji"></span><span class="executive-card__model-text"><strong>Anthropic Claude</strong> </span></li>
        <li><span class="executive-card__emoji"></span><span class="executive-card__model-text"><strong>Google Gemini </strong> </span></li>
        <li><span class="executive-card__emoji"></span><span class="executive-card__model-text"><strong>Mistral Large</strong> </span></li>
        <li><span class="executive-card__emoji"></span><span class="executive-card__model-text"><strong>Ollama</strong> (locally hosted models in secure private clouds for sensitive workloads.)</span></li>
      </ul>

    </div>
  </div>
  <div class="executive-card__section executive-card__section--full">
    <h3>Why It Matters for Business Leaders</h3>
    <ul class="executive-card__benefits">
      <li><strong>De-risk AI rollouts</strong> — start with explainable, citation-backed answers instead of black-box chatbots.</li>
      <li><strong>Accelerate time to value</strong> — launch pilot use cases in days, not quarters, with governance baked in.</li>
      <li><strong>Scale with confidence</strong> — observability dashboards surface adoption, accuracy, and compliance trends for every release.</li>
    </ul>
    <a
      class="executive-card__cta executive-card__cta--dark"
      href="https://synapsefluxlab.pages.dev/#contactform"
      target="_blank"
      rel="noopener noreferrer"
    >
      Talk with RAG Loom team
    </a>
  </div>
</div>


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
