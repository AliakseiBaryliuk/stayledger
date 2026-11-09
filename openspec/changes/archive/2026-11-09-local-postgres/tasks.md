# Tasks

## 1. PostgreSQL Helm release configuration

- [x] 1.1 Add `deploy/helm/postgresql/values-local.yaml` for Bitnami PostgreSQL chart 18.7.12 with the standalone topology, `stayledger` namespace naming, external Secret mapping, persistent ReadWriteOnce storage, and retain-on-delete PVC policy; verify `helm template stayledger oci://registry-1.docker.io/bitnamicharts/postgresql --version 18.7.12 --namespace stayledger --values deploy/helm/postgresql/values-local.yaml` renders a PostgreSQL workload, Service, PVC, and Secret references without credential values.
- [x] 1.2 Set the application chart's local Secret name and key mapping to the shared `stayledger-runtime` contract if it is not already exact; verify `helm template` with both local values renders `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` as Secret references and contains no literal credentials.

## 2. Local PostgreSQL operations documentation

- [x] 2.1 Add `deploy/helm/postgresql/README.md` documenting the chart OCI source, chart version, digest, release/service name, database/user names, Secret keys, and a PowerShell Secret-creation command that reads all values from operator environment variables; verify the command and YAML values contain no real credential.
- [x] 2.2 Document the database install/upgrade, readiness, authenticated connection diagnostics, application rollout, and rollback commands; verify every command uses `stayledger` namespace and the JDBC URL uses the PostgreSQL Service DNS name rather than `localhost`.
- [x] 2.3 Document ordinary non-destructive uninstall and the separately marked intentional PVC-removal procedure, including the exact PVC discovery command and data-loss warning; verify the standard cleanup commands do not delete a PersistentVolumeClaim.

## 3. Minikube integration verification

- [x] 3.1 Run the documented Minikube storage preflight and install the PostgreSQL release on a driver with a compatible StorageClass; verify the PostgreSQL workload is ready and its PVC is `Bound`.
- [x] 3.2 Create the runtime Secret outside Git and deploy the existing StayLedger Helm release against the database Service DNS; verify both Helm rollouts complete and the application Deployment exposes only Secret references for its database environment variables.
- [x] 3.3 Exercise the documented database connection diagnostic and normal release cleanup; verify the diagnostic can reach the database and the PVC remains after a non-destructive release removal.
