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
with `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` keys. Supply the values through
your secure shell or secret-management workflow; do not place them in a values
file or commit them to Git. After the three environment variables are set in
the current PowerShell session, create the Secret in the application namespace:

```powershell
kubectl create namespace stayledger --dry-run=client -o yaml | kubectl apply -f -
kubectl --namespace stayledger create secret generic stayledger-runtime `
  --from-literal=DB_URL="$env:DB_URL" `
  --from-literal=DB_USERNAME="$env:DB_USERNAME" `
  --from-literal=DB_PASSWORD="$env:DB_PASSWORD"
```

Use `--dry-run=client -o yaml | kubectl apply -f -` for the Secret command if
you need an idempotent update. The chart supports different Secret names and
key names through `existingSecret.name` and `existingSecret.keys` values.

## Local validation and install

The local values file points at the local Nexus image repository and contains
only its image coordinate and external Secret name. Validate and render it:

```powershell
helm lint deploy/helm/stayledger --values deploy/helm/stayledger/values-local.yaml
helm template stayledger deploy/helm/stayledger `
  --namespace stayledger `
  --values deploy/helm/stayledger/values-local.yaml
```

Install or update the application release after the image is available to the
cluster and the external Secret exists:

```powershell
helm upgrade --install stayledger deploy/helm/stayledger `
  --namespace stayledger `
  --create-namespace `
  --values deploy/helm/stayledger/values-local.yaml
```

For a repeatable deployment, pass the exact immutable image built by delivery
automation instead of editing chart files:

```powershell
helm upgrade --install stayledger deploy/helm/stayledger `
  --namespace stayledger `
  --create-namespace `
  --values deploy/helm/stayledger/values-local.yaml `
  --set-string image.repository=localhost:5000/stayledger `
  --set-string image.tag=<built-version>
```

To roll back an unsuccessful release, run
`helm rollback stayledger <revision> --namespace stayledger`.
