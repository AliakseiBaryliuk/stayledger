# Stage 3 — Application Helm Chart

**Proposed branch:** `feature/helm-application`
**Dependencies:** stages 1–2

## Objective

Add a Helm chart to install the application without secrets in Git and with support for safe updates.

## Changes

- Create the chart in `deploy/helm/stayledger`, since the repository has no convention yet for Kubernetes artifact placement.
- Add a Deployment, ClusterIP Service, ConfigMap for non-sensitive settings, and references to an existing Kubernetes Secret for sensitive variables.
- Configure labels, requests/limits, rollout strategy, Actuator liveness/readiness probes, and image repository/tag values.
- Create shared values and local-environment values. Do not add real passwords or encoded Secret values to the repository.
- Support `helm upgrade --install`, `helm lint`, and `helm template`; use an application namespace.

## Out of Scope

- Provisioning PostgreSQL, a Secret with real values, the Minikube lifecycle, and monitoring.

## Acceptance Criteria

- `helm lint` and `helm template` pass with local values.
- The rendered Deployment contains no passwords, and image and tag are configurable through Helm parameters.
- Probes target the endpoints actually enabled in stage 1.
