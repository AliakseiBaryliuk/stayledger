# Tasks

## 1. Define the reproducible local deployment path

- [x] 1.1 Replace the Stage 5 outline in `docs/cicd-kubernetes/05-minikube-runbook.md` with a PowerShell runbook for tool prerequisites, `minikube start`, context/profile verification, namespace creation, and StorageClass preflight; verify every referenced executable has a version or status command and the PostgreSQL preflight checks a compatible dynamic RWO StorageClass before installation.
- [x] 1.2 Document exact-version image preparation from the existing local Nexus coordinate and delivery with `minikube image load`; verify the runbook uses identical repository/tag values for Docker inspection, image loading, and the Helm application override, and explicitly states that the Minikube node cannot rely on host `localhost:5000`.

## 2. Document deployment, verification, and recovery

- [x] 2.1 Add the ordered runtime Secret, pinned PostgreSQL release, application `helm upgrade --install`, and rollout procedures using the existing `stayledger` namespace and release contracts; verify the documented order creates the Secret before either release and waits for both PostgreSQL and application readiness.
- [x] 2.2 Add a Service `kubectl port-forward` smoke check against the readiness endpoint; verify the documented command targets the existing ClusterIP Service and identifies port-forward as a foreground process to stop after the check.
- [x] 2.3 Add failure diagnostics for locally loaded images, Pods/Deployments/Services, namespace Events, PostgreSQL logs, and authenticated in-Pod database connectivity; verify each acceptance-criterion failure class has an executable diagnostic command.
- [x] 2.4 Add Helm history/rollback and cleanup instructions that retain the PostgreSQL PVC by default and isolate PVC deletion in an explicit destructive section; verify normal cleanup contains no `kubectl delete pvc` command.

## 3. Validate the runbook boundaries and usability

- [x] 3.1 Cross-check the final commands and identifiers against `docs/cicd-kubernetes/02-versioning-and-docker.md`, `deploy/helm/postgresql/README.md`, and `deploy/helm/stayledger/README.md`; verify image coordinates, Secret keys, release names, namespace, Service DNS, and health endpoint agree.
- [x] 3.2 Review the completed runbook from an empty Minikube cluster perspective and record only supported local Minikube assumptions; verify it excludes Jenkins automation and Prometheus/Grafana installation while linking or referring to their separate stages where useful.
