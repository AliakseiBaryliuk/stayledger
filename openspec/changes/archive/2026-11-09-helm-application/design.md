# Design

## Context

See `proposal.md` for motivation and
`specs/helm-application-deployment/spec.md` for the deployment contract.
StayLedger presently builds the database-free application image
`localhost:5000/stayledger:<version>`, listens on port 8081, and exposes the
Actuator liveness and readiness paths required by the chart. No Kubernetes or
Helm assets currently exist. Database infrastructure and Secret creation are
explicitly deferred to later stages.

## Goals / Non-Goals

**Goals:**

- Provide a Helm v3 chart that can render and install a single application
  replica safely in an operator-selected namespace.
- Keep the image coordinates, runtime resources, rollout policy, and
  non-sensitive settings configurable through values.
- Keep credentials outside the chart while retaining the exact environment
  variable contract already used by the application.

**Non-Goals:**

- Create a Namespace, PostgreSQL workload, PersistentVolumeClaim, Ingress,
  monitoring stack, or Kubernetes Secret resource.
- Change Spring Boot configuration, database connectivity semantics, or the
  Gradle/Docker versioning contract.
- Automate Minikube image loading, cluster lifecycle, or CI/CD deployment.

## Decisions

### Helm chart owns only application resources

Place a Helm v2 chart API definition at `deploy/helm/stayledger` with standard
helper templates for release-scoped names and recommended Kubernetes labels.
The chart renders the Deployment, ClusterIP Service, and ConfigMap only. It
uses `.Release.Namespace`; namespace creation remains a Helm CLI/operator
concern (`--namespace` and `--create-namespace`) so every rendered resource has
one namespace authority.

Creating a `Namespace` template was considered, but it conflicts with
operator-controlled namespaces and makes lifecycle ownership ambiguous.

### Values separate portable defaults from local delivery settings

`values.yaml` supplies portable application defaults: one replica, port 8081,
rolling-update parameters, resource requests/limits, probe timing, and the
non-sensitive configuration exposed by the ConfigMap. A local values file
selects the loopback Nexus repository and a locally built image tag solely for
local validation and installation. Automation can override `image.repository`
and `image.tag` with the exact immutable build reference; the chart does not
derive or calculate application versions.

The local values file is intentionally an environment input rather than a
second versioning mechanism. Duplicating Gradle's version calculation in Helm
was rejected because it can make JAR and image identities diverge.

### Explicit environment wiring preserves the secret boundary

The ConfigMap holds supported non-sensitive environment variables, initially
`SERVER_PORT`. The Deployment consumes it through a ConfigMap reference. Three
explicit `secretKeyRef` entries supply `DB_URL`, `DB_USERNAME`, and
`DB_PASSWORD`; values configure the Secret name and key names, while the chart
uses `required` validation for the Secret name. The chart never declares a
`Secret` template and never accepts credential values as Helm values.

`envFrom` for the Secret was considered, but explicit mappings document the
application contract and allow the external Secret's key names to differ
without injecting unrelated values.

### Deployment is health-aware and conservative by default

The Deployment sets a `RollingUpdate` strategy with configurable
`maxUnavailable` and `maxSurge`, resource requests and limits, and a named
container port at 8081. Its probes use the runtime-observability contract:
`/actuator/health/liveness` and `/actuator/health/readiness` on that port. The
Service uses the same selector labels and forwards its application port to the
named container port.

Using `/actuator/health` for both probes was rejected because it does not
distinguish process liveness from readiness.

## Risks / Trade-offs

- [Image is unavailable inside the cluster] -> Keep image coordinates
  configurable and document that Minikube image loading is handled by Stage 5.
- [External Secret is missing or keys are incorrect] -> Require the Secret name
  at render time and rely on Kubernetes Pod diagnostics for absent keys; Stage 4
  will document and create the database Secret outside Git.
- [A local tag becomes stale] -> Treat local values as a validation example and
  override the tag with the exact build version in repeatable deployments.
- [One replica cannot provide service continuity] -> Preserve a safe rolling
  policy for future replica increases; high availability is outside this stage.

## Migration Plan

1. Add chart metadata, reusable name and label helpers, default values, and
   local values.
2. Add the ConfigMap, Deployment, and Service templates with externally managed
   Secret references.
3. Validate the chart with `helm lint` and render it with local values.
4. Install or update with `helm upgrade --install --namespace <application-ns>
   --create-namespace`; an operator creates the referenced Secret separately.
5. Roll back an unsuccessful update with `helm rollback <release> <revision>`
   or uninstall the release. Neither operation deletes an externally managed
   Secret.
