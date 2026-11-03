# Local CI/CD and Kubernetes Specifications

These are review specifications to be approved before creating OpenSpec changes. They neither replace OpenSpec capability specifications nor authorize implementation.

| Stage | Specification | Depends on |
| --- | --- | --- |
| 1 | [Application runtime and observability](01-runtime-observability.md) | — |
| 2 | [Versioning and Docker](02-versioning-and-docker.md) | 1 |
| 3 | [Application Helm chart](03-helm-application.md) | 1, 2 |
| 4 | [PostgreSQL on Kubernetes](04-postgresql.md) | 3 |
| 5 | [Minikube runbook](05-minikube-runbook.md) | 3, 4 |
| 6 | [Jenkins pipeline](06-jenkins-pipeline.md) | 1–5 |
| 7 | [Prometheus and Grafana](07-monitoring.md) | 1, 3 |

Each stage is implemented in its own branch from `stayledger-codex-develop` and delivered through a separate PR to that branch. A production delivery is later promoted through a `release/RL-xx` branch; develop never merges directly into `stayledger-codex`. A separate OpenSpec change is created after stage review; no application or infrastructure changes are made before that.
