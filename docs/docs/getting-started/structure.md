---
id: structure
title: Project Structure
sidebar_position: 3
---

Understanding the repository layout accelerates onboarding and clarifies where to add new functionality or configuration.

```
rag-loom/
├── app/
│   ├── api/             # FastAPI routers and request/response models
│   ├── core/            # Application bootstrapping and settings
│   ├── models/          # Domain and persistence models
│   ├── services/        # Ingestion, retrieval, generation pipelines
│   └── utils/           # Shared helpers (I/O, logging, instrumentation)
├── docs/
│   ├── docs/            # Docusaurus Markdown sources (this site)
│   ├── src/             # Custom pages, CSS, and theme overrides
│   └── static/          # Assets exposed by the site (images, downloads)
├── tests/               # Unit, integration, and end-to-end tests
├── utilscripts/         # Operational utilities (quick start, docs tooling)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image for deployment
└── start_production.sh  # Entry point for the production docker-compose stack
```

### Configuration Files

| File | Purpose |
| --- | --- |
| `.env` | Runtime configuration for local development |
| `env.production` | Baseline production configuration |
| `pytest.ini` | Pytest defaults and markers |
| `Dockerfile` | Builds the application image with production dependencies |

### Scripts & Automation

| Script | Location | Description |
| --- | --- | --- |
| `quick_start.sh` | `utilscripts/` | One-stop install, start, test workflow |
| `docs_start.sh` | `utilscripts/` | Spins up the Docusaurus dev server |
| `docs_build.sh` | `utilscripts/` | Produces static documentation assets |
| `start_production.sh` | repo root | Boots the docker-compose production topology |

### Tests

- `tests/unit/`: Functional units and helpers.
- `tests/integration/`: Multi-component workflows.
- `test_service.py`: REST API smoke tests executed during CI.

With the structure in mind, explore the [Architecture overview](../architecture/system-design) to see how these components interact at runtime.
