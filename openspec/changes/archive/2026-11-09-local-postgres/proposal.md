# Proposal

## Why

The application Helm chart can consume database settings from an externally
managed Secret, but no local Kubernetes PostgreSQL service or persistent
storage exists to supply those settings. A version-pinned PostgreSQL release is
needed before a developer can deploy the application to Minikube with an
in-cluster database and without committing credentials.

## What Changes

- Add a version-pinned Bitnami PostgreSQL Helm release for the application
  namespace, configured as a single primary with persistent storage.
- Define the operator-managed Secret contract used by both PostgreSQL and the
  existing application Helm chart, including the application JDBC URL through
  the PostgreSQL Service DNS name.
- Add local deployment values and documentation for Secret creation, database
  and application rollout verification, connection diagnostics, upgrades, PVC
  retention, and intentional data removal.
- Verify the rendered PostgreSQL resources and the local Minikube deployment
  path without adding JPA entities, schema migrations, or a PostgreSQL
  exporter.

## Capabilities

### New Capabilities

- `postgresql-kubernetes-deployment`: Provision and operate the local,
  persistent PostgreSQL service that supplies the application database
  connection on Kubernetes.

### Modified Capabilities

- None.

## Impact

- Adds a PostgreSQL Helm values/configuration asset and local operational
  documentation under the existing Kubernetes deployment structure.
- Uses a pinned external Bitnami PostgreSQL Helm chart and Kubernetes Secret,
  Service, StatefulSet, and PersistentVolumeClaim resources.
- Reuses the existing StayLedger Helm chart's `existingSecret` mapping and the
  application's `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` environment
  variables; no application-domain behavior or public HTTP API changes.
