# Stage 7 — Prometheus and Grafana

**Proposed branch:** `feature/cluster-monitoring`  
**Dependencies:** stages 1 and 3

## Objective

Collect Kubernetes and application metrics in Prometheus and make them available through Grafana in the local cluster.

## Changes

- Install a version-pinned `kube-prometheus-stack` in a dedicated monitoring namespace with reasonable Minikube requests/limits.
- Create a ServiceMonitor for the application Service with labels compatible with the Prometheus Operator selector and the `/actuator/prometheus` endpoint.
- Keep application metrics internal: do not create a separate external Service or ingress for Actuator.
- Document `kubectl port-forward` for Grafana, Prometheus target verification, and querying an application metric.
- Do not install a PostgreSQL exporter in this stage; add it only in a separate specification when there is a real need and a secure credential source.

## Out of Scope

- Production retention and backup policies, alert routing, and dashboard-as-code beyond minimal operational verification.

## Acceptance Criteria

- The application Prometheus target has `UP` status and receives metrics from `/actuator/prometheus`.
- Grafana is available through port-forward and uses the Prometheus data source.
- The monitoring installation contains no Grafana or PostgreSQL credentials in Git.
