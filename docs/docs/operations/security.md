---
id: security
title: Security Hardening
sidebar_position: 4
---

Secure configuration is essential when RAG Loom handles sensitive data. This checklist covers authentication, network controls, and operational safeguards.

## Authentication & Authorisation

- Enable the optional authentication middleware by setting `ENABLE_AUTH=true` and implementing the token validation hook.
- Protect administrative endpoints (e.g., `/docs`, `/metrics`) behind an identity-aware proxy or API gateway.
- Rotate API keys and secrets periodically; avoid committing them to source control.

## Network Controls

- Expose only the required ports externally. Keep vector stores, Redis, Ollama, Prometheus, and Grafana on private networks.
- Use a reverse proxy (Nginx, Traefik, AWS ALB) to terminate TLS and enforce rate limiting.
- Apply firewall rules or security groups allowing access solely from trusted IP ranges or VPCs.

## Secrets Management

- Store secrets in a vault (AWS Secrets Manager, HashiCorp Vault) or orchestrator-specific facility (Kubernetes secrets).
- For local development, keep `.env` files outside version control and restrict file permissions (`chmod 600 .env`).

## Data Protection

- If ingesting sensitive documents, encrypt data at rest (disk-level encryption or encrypted volumes).
- Sanitise or redact logged content before storing in centralised logging systems.
- Implement retention policies for both original documents and vector embeddings.

## Monitoring & Audit

- Enable metrics (`ENABLE_METRICS=true`) and integrate with alerting platforms to detect anomalies.
- Capture audit logs for ingestion and generation events, including user identifiers where appropriate.
- Establish incident response procedures and practice disaster recovery (coordinate with the runbooks in [Scaling](./scaling) and [Troubleshooting](./troubleshooting)).

## Dependency Management

- Run `pip list --outdated` routinely and apply security patches promptly.
- Scan container images (e.g., with Trivy, Grype) as part of CI/CD pipelines.
- Validate third-party model downloads (checksums, source authenticity).

## Compliance Considerations

- Evaluate regulatory requirements (GDPR, HIPAA, SOC 2) for your use case.
- Classify documents by sensitivity and restrict ingestion paths accordingly.
- Document access controls and review them periodically.

For operational incidents or service instability, refer to [Troubleshooting](./troubleshooting). Combine these practices with organisational policies to meet your compliance baseline.
