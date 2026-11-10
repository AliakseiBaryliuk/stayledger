# Design

## Context

See `proposal.md` for the motivation. The repository already defines a local
Nexus registry at `localhost:5000`, a StayLedger chart that uses
`IfNotPresent`, and a pinned PostgreSQL release with an operator-managed
runtime Secret. Those documents are individually usable, but they do not
define the complete Minikube lifecycle or make the image-delivery boundary
explicit.

## Goals / Non-Goals

**Goals:**

- Provide one PowerShell-oriented path from an empty Minikube cluster to a
  locally reachable StayLedger application.
- Make each command's prerequisite and expected result observable.
- Reuse the existing image, Secret, Helm release, Service DNS, and PVC
  contracts without duplicating their configuration.

**Non-Goals:**

- Change the application, Docker image build/publish workflow, Helm charts,
  PostgreSQL values, or Kubernetes resource definitions.
- Make Minikube pull from the host's loopback Nexus registry.
- Automate the procedure in Jenkins or install monitoring components.

## Decisions

### Keep Nexus as the image source and load the exact image into Minikube

The runbook will use the versioned local image coordinate
`localhost:5000/stayledger:<version>`, verify that Docker has that exact image,
and run `minikube image load` for it before the application release is
installed. The Helm command will pass the same repository and tag explicitly.

This separates registry publication from node image availability. It works
across Minikube drivers and does not treat the node's `localhost` as the host
Nexus endpoint. Using a shared Docker daemon is rejected because it is
driver-dependent; configuring an in-cluster pull path to host Nexus is
rejected because it adds networking and trust setup outside the local runbook.

### Make the runbook a linear, idempotent operator path

The document will order actions as: prerequisites and version checks,
`minikube start`, context/profile verification, namespace and StorageClass
preflight, image load, runtime Secret, PostgreSQL install/readiness,
application install/rollout, then port-forward smoke check. Namespace and
Secret operations use the existing idempotent forms where provided; Helm uses
`upgrade --install`.

This order avoids an application Pod attempting to start before its image,
database, and Secret exist. A collection of independent command snippets is
rejected because it leaves ordering and failure handling ambiguous for a new
developer.

### Use the existing release contracts rather than duplicate their commands

The runbook will reference the pinned PostgreSQL chart/version, Secret key
contract, `stayledger` namespace, database Service DNS, and Helm release names
from the existing deployment guides. It may repeat the commands required for a
complete run, but it will identify the existing documents as the authority for
chart-specific credential updates and intentional PVC deletion.

This gives one usable path while avoiding divergent copies of chart values or
credentials. A separate Minikube-specific chart configuration is rejected
because the current chart supports the local deployment unchanged.

### Treat smoke checks and diagnostics as first-class outcomes

After rollout, the document will port-forward the ClusterIP Service to a local
port and check the existing readiness endpoint. Failure branches will cover
local image inspection and Minikube image cache verification, Pods/Deployments/
Services, namespace Events, PostgreSQL logs and in-Pod `psql`, Helm history and
rollback. Normal cleanup will uninstall releases and show retained PVCs;
deleting a PVC remains an explicit destructive procedure.

This verifies the externally usable application rather than only resource
creation. A Pod-only health check is rejected because it does not verify
Service routing from the developer's machine.

## Risks / Trade-offs

- [The requested image is absent from the local Docker store or Minikube cache]
  -> Verify the exact image coordinate before and after `minikube image load`;
  reinstall/upgrade only after it is available.
- [No compatible dynamic ReadWriteOnce StorageClass is available] -> Stop at
  the StorageClass preflight and select a compatible driver or StorageClass;
  do not proceed with a non-persistent database.
- [The local Nexus endpoint is mistaken for a node-reachable registry] -> State
  that Nexus is a local image source and require image loading into Minikube.
- [A local Secret value or existing database data is unintentionally replaced]
  -> Never print credentials, retain normal PVC cleanup, and link to the
  existing deliberate password/PVC procedures.
- [A port-forward process remains active after the smoke check] -> Document it
  as a foreground, user-terminated process and distinguish it from deployment
  state.

## Migration Plan

1. Add the runbook as documentation only; no cluster migration is required.
2. Validate the documented commands against an empty Minikube cluster and an
   exact locally available image.
3. If an upgrade fails, use Helm history and roll back only the affected
   release; retain the PostgreSQL PVC during normal cleanup.
