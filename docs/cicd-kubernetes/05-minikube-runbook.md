# Stage 5 — Minikube Runbook

**Proposed branch:** `chore/minikube-runbook`  
**Dependencies:** stages 3–4

## Objective

Make local installation reproducible before Jenkins is introduced, and explicitly document the boundaries of Minikube support.

## Changes

- Document Docker, Minikube, kubectl, and Helm prerequisites, namespace creation, and cluster startup order.
- Use `minikube image load` to deliver a locally built image into the cluster; do not assume a shared Docker daemon across drivers and Jenkins.
- Document Secret creation, PostgreSQL installation, application `helm upgrade --install`, rollout waiting, and smoke checking through `kubectl port-forward`.
- Add diagnostic commands for Pods, Services, Events, and PostgreSQL, as well as Helm release rollback and safe cleanup without implicit PVC deletion.

## Out of Scope

- Jenkins automation and Prometheus/Grafana installation.

## Acceptance Criteria

- A new developer can progress from an empty Minikube cluster to an available application by following the documented commands.
- Image delivery, readiness, and database connection failures have explicit diagnostic commands.
