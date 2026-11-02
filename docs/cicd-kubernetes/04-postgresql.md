# Stage 4 — PostgreSQL on Kubernetes

**Proposed branch:** `feature/local-postgres`
**Dependencies:** stage 3

## Objective

Prepare a local PostgreSQL installation for Helm deployment of the application, with persistent data and secure credential delivery.

## Changes

- Select a supported, version-pinned PostgreSQL Helm chart in the OpenSpec design; record its source, version, existing Secret keys, and upgrade procedure.
- Deploy the database in the application namespace with a PVC, and have the application connect through Kubernetes Service DNS rather than `localhost`.
- Provide a documented command to create the Secret outside Git. The chart receives credentials only through the selected version's documented contract.
- Pass the URL, user, and password to the application through environment variables and Secret references; verify database readiness and successful application rollout.
- Document connection diagnostics, PVC retention, and intentional PVC removal.

## Out of Scope

- JPA entities and schema migrations: the current project has no scenario using the database. When one is introduced, migrations are implemented in its own OpenSpec change.
- PostgreSQL exporter.

## Acceptance Criteria

- PostgreSQL uses a PVC when supported by the selected Minikube driver.
- Git contains no real credentials.
- The running application receives its settings through Service DNS and completes rollout successfully when the database is available.
