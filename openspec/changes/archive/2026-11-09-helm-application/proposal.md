# Proposal

## Why

StayLedger has a versioned, runnable OCI image but no reproducible Kubernetes
application deployment. A Helm chart is needed now to make local cluster
installation and safe application updates possible without committing runtime
credentials.

## What Changes

- Add a Helm chart for the StayLedger application under `deploy/helm/stayledger`.
- Render a Deployment, ClusterIP Service, and ConfigMap for non-sensitive
  runtime settings.
- Reference a pre-existing Kubernetes Secret for database environment
  variables without defining secret values in source control.
- Make image repository and tag, resource requests and limits, rollout
  settings, and non-sensitive configuration configurable through values.
- Configure liveness and readiness probes for the Actuator endpoints already
  provided by the runtime-observability capability.
- Provide shared defaults and local-environment values, plus chart validation
  guidance for `helm lint`, `helm template`, and `helm upgrade --install` in
  an application namespace.

## Capabilities

### New Capabilities

- `helm-application-deployment`: install and upgrade the application on
  Kubernetes through a configurable Helm release while keeping sensitive
  settings in an externally managed Secret.

### Modified Capabilities

- None.

## Impact

- Adds Helm chart assets under `deploy/helm/stayledger` and local values for
  cluster use.
- Consumes the existing `localhost:5000/stayledger:<version>` image delivery
  contract and the HTTP health endpoints on port 8081.
- Introduces Helm as a development and delivery prerequisite, but does not
  provision PostgreSQL, create Secret values, or change application code.
