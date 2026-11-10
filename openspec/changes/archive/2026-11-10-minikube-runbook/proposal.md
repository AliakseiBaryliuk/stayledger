# Proposal

## Why

The application and local PostgreSQL Helm releases are available, but a new
developer has no single, driver-independent procedure for delivering a built
image to Minikube and verifying the complete local stack. A runbook is needed
before Jenkins automation can reuse and automate those validated commands.

## What Changes

- Add a local Minikube runbook covering prerequisites, profile startup,
  namespace/storage preflight, and deployment order.
- Define image delivery from the local Docker image store to the Minikube node
  with `minikube image load`; do not rely on a shared Docker daemon or on
  `localhost:5000` being reachable from the node.
- Consolidate the existing runtime Secret, PostgreSQL release, StayLedger Helm
  release, rollout, and port-forward smoke-check procedures into one operator
  path.
- Add diagnostics for image availability, Kubernetes workloads, Services,
  Events, PostgreSQL connectivity, Helm rollback, and non-destructive cleanup.
- State the support boundary: this runbook is for a local Minikube deployment,
  not Jenkins automation or Prometheus/Grafana installation.

## Capabilities

### New Capabilities

None. This change documents operating procedures for already specified
delivery, Helm deployment, and PostgreSQL capabilities; it introduces no new
product behavior.

### Modified Capabilities

None. Existing capability requirements already cover the chart and database
contracts consumed by this runbook.

## Impact

- Adds the Stage 5 Minikube runbook under `docs/cicd-kubernetes/`.
- Relies on the existing local Nexus image coordinate, Helm charts, runtime
  Secret contract, and PostgreSQL Service DNS contract.
- Does not modify application code, Helm templates, image publication, or
  external runtime dependencies.
