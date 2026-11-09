# Design

## Context

See `proposal.md` for motivation. The existing `deploy/helm/stayledger` chart
deploys the application and reads `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD`
from an external Secret. `_ms` maps these variables to Spring datasource
properties, but the current scope adds neither persistence behavior nor schema
migrations. No local database Helm release or deployment runbook currently
exists.

## Goals / Non-Goals

**Goals:**

- Give the local Kubernetes deployment one persistent PostgreSQL primary with a
  stable in-cluster Service name.
- Keep all password values outside Git while making one documented Secret
  contract usable by both charts.
- Make install, verification, diagnostics, safe upgrade, and intentional data
  deletion reproducible for a supported Minikube storage configuration.

**Non-Goals:**

- Adding JPA, a domain persistence mini-scenario, schema migrations, backups,
  replication, TLS, or a PostgreSQL exporter.
- Treating the existing application readiness endpoint as a database-connectivity
  check; the current runtime capability deliberately starts without database
  access.

## Decisions

### Use the Bitnami PostgreSQL OCI chart 18.7.12

Install `oci://registry-1.docker.io/bitnamicharts/postgresql` with
`--version 18.7.12` (digest
`sha256:6ce4a9dea4153dc5e3b48a24739df5c89bab5797f1a69bf5ac1ce30f9980be02`).
This exact chart version was inspected for its Secret and persistence contract.
Use `architecture: standalone`; local development does not need replicas.

The local values shall explicitly configure `primary.persistence.enabled: true`,
ReadWriteOnce storage, a driver-compatible StorageClass (or its default), and
`primary.persistentVolumeClaimRetentionPolicy` with `enabled: true` and both
retention actions set to `Retain`. The chart creates the database Service; the
application URL will target that Service name on port 5432.

Bitnami provides the ready-to-operate StatefulSet, probes, Service, and PVC
contract needed here. Writing a bespoke PostgreSQL StatefulSet would create
unnecessary lifecycle and credential-management responsibility. A PostgreSQL
operator is unnecessary for one local primary and would add a prerequisite
outside the stage scope.

### Use one operator-managed runtime Secret

The operator creates `stayledger-runtime` in namespace `stayledger` outside
Git. It contains `postgres-password` and `password`, consumed by Bitnami via
`auth.existingSecret` and its documented default keys, plus `DB_URL`,
`DB_USERNAME`, and `DB_PASSWORD`, consumed by the existing application chart.
`DB_PASSWORD` is created from the same supplied value as `password`; the two
key names are required by the independent chart contracts. `DB_URL` has the
form `jdbc:postgresql://stayledger-postgresql:5432/stayledger` and never uses
`localhost`.

One Secret avoids password drift in a local environment. Separate database and
application Secrets were considered for stronger separation, but they require
securely synchronizing the same password and add no practical benefit to this
single-namespace local setup. The Secret command receives values only from the
operator environment; values files hold names and key mappings only.

### Keep database assets separate from the application chart

Add PostgreSQL local values and operator documentation under
`deploy/helm/postgresql/`. The Bitnami OCI chart stays external rather than
being vendored into the application chart. The existing
`deploy/helm/stayledger` chart remains responsible only for the application;
its local values will select `stayledger-runtime` and retain its explicit
Secret key mapping.

This preserves the stage-3 ownership boundary and lets the database release be
installed, upgraded, and removed independently.

### Verify infrastructure rather than invent application persistence behavior

Validation renders the pinned PostgreSQL chart and the existing application
chart, then uses Minikube/Kubernetes rollout commands to verify the database
and application workloads. Diagnostics inspect Pods, Events, Service endpoints,
PVC/PV state, and PostgreSQL logs. A short-lived authenticated client check may
verify the database endpoint; it does not add application code or a migration.

## Risks / Trade-offs

- [A Minikube driver has no compatible dynamic StorageClass] -> Document the
  storage preflight and state that persistence is only validated where the
  driver supports the selected PVC mode.
- [Credentials differ from the data already initialized in a retained PVC] ->
  Document that credentials are initialized with the database data; use the
  chart's documented password-update process or intentionally remove the PVC
  only when data loss is accepted.
- [The external chart or image changes] -> Pin the chart version and OCI digest
  in documentation, verify rendering before upgrades, and review chart release
  notes before changing either pin.
- [A retained PVC survives a release uninstall] -> Make ordinary cleanup
  non-destructive and place the explicit PVC deletion command in a separately
  marked destructive-cleanup section.

## Migration Plan

1. Check the active Minikube StorageClass and create the `stayledger` namespace.
2. Create `stayledger-runtime` from operator-supplied environment values.
3. Install or upgrade the pinned PostgreSQL release with local values; wait for
   the database workload and PVC to become ready/bound.
4. Install or upgrade the existing StayLedger application chart with its local
   values; wait for rollout and inspect application Secret references.
5. For rollback, roll back Helm revisions without deleting the PVC. For a
   deliberate fresh database, uninstall the database release and delete the
   identified PVC only after accepting data loss.
