# StayLedger Helm chart

This chart deploys the StayLedger application into the namespace selected by
the Helm release. It creates a Deployment, ClusterIP Service, and ConfigMap;
it does not create a Kubernetes Secret or database workload.

## Prerequisites

- Helm 3 or later
- `kubectl` access to the target cluster
- An application image available to that cluster
- An externally managed Secret containing the database configuration

## External Secret

The local values file expects an existing Secret named `stayledger-runtime`
with `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` keys. When PostgreSQL is
deployed locally, that Secret also supplies the PostgreSQL chart's password
keys. Create it through a secure shell or secret-management workflow; do not
place values in a chart values file or commit them to Git. See the
[local PostgreSQL release guide](../postgresql/README.md#runtime-secret) for
the complete key contract and idempotent PowerShell command. The chart supports
different Secret names and key names through `existingSecret.name` and
`existingSecret.keys` values.

## Local validation and install

The local values file points at the local Nexus image repository and contains
only its image coordinate and external Secret name. Validate and render it:

```powershell
helm lint deploy/helm/stayledger --values deploy/helm/stayledger/values-local.yaml
helm template stayledger-app deploy/helm/stayledger `
  --namespace stayledger `
  --values deploy/helm/stayledger/values-local.yaml
```

Install or update the application release after the image is available to the
cluster and the external Secret exists:

```powershell
helm upgrade --install stayledger-app deploy/helm/stayledger `
  --namespace stayledger `
  --create-namespace `
  --values deploy/helm/stayledger/values-local.yaml
```

For a repeatable deployment, pass the exact immutable image built by delivery
automation instead of editing chart files:

```powershell
helm upgrade --install stayledger-app deploy/helm/stayledger `
  --namespace stayledger `
  --create-namespace `
  --values deploy/helm/stayledger/values-local.yaml `
  --set-string image.repository=localhost:5000/stayledger `
  --set-string image.tag=<built-version>
```

To roll back an unsuccessful application release, run
`helm rollback stayledger-app <revision> --namespace stayledger`.
