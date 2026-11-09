# Local PostgreSQL Helm release

This directory configures the local StayLedger PostgreSQL release. It uses the
Bitnami PostgreSQL OCI chart, not a vendored chart.

## Release contract

| Item | Value |
| --- | --- |
| OCI chart | `oci://registry-1.docker.io/bitnamicharts/postgresql` |
| Chart version | `18.7.12` |
| Chart digest | `sha256:6ce4a9dea4153dc5e3b48a24739df5c89bab5797f1a69bf5ac1ce30f9980be02` |
| Helm release / namespace | `stayledger` / `stayledger` |
| PostgreSQL Service | `stayledger-postgresql` |
| Database / application user | `stayledger` / `stayledger` |
| Application JDBC URL | `jdbc:postgresql://stayledger-postgresql:5432/stayledger` |

The local values configure a standalone primary, an 8 Gi ReadWriteOnce PVC, and
retention of that PVC when the StatefulSet is removed or scaled down. The empty
`primary.persistence.storageClass` value lets a compatible Minikube default
StorageClass provision it. Set a specific compatible StorageClass with
`--set-string primary.persistence.storageClass=<name>` if the cluster has no
default.

## Prerequisites and storage preflight

Install Minikube, `kubectl`, and Helm 3. Start the intended Minikube profile,
then confirm that its storage provisioner can bind ReadWriteOnce claims before
installing PostgreSQL:

```powershell
minikube status
kubectl get storageclass
kubectl get storageclass -o custom-columns=NAME:.metadata.name,DEFAULT:.metadata.annotations.storageclass\.kubernetes\.io/is-default-class,PROVISIONER:.provisioner
kubectl create namespace stayledger --dry-run=client -o yaml | kubectl apply -f -
```

Use a driver and StorageClass that support dynamic ReadWriteOnce PVCs. If no
compatible class is available, do not continue with the persistent local
database installation.

## Runtime Secret

The releases share one externally managed `stayledger-runtime` Secret. It must
contain these keys:

| Key | Consumer |
| --- | --- |
| `postgres-password` | PostgreSQL `postgres` administrator |
| `password` | PostgreSQL `stayledger` user |
| `DB_URL` | StayLedger application datasource URL |
| `DB_USERNAME` | StayLedger application datasource username |
| `DB_PASSWORD` | StayLedger application datasource password; same value as `password` |

Set `POSTGRES_PASSWORD` and `DB_PASSWORD` through a secure operator workflow;
the repository does not supply their values. The following command reads them
from the current PowerShell environment and creates or updates the Secret
without putting credentials in Helm values:

```powershell
$runtimeDbUrl = 'jdbc:postgresql://stayledger-postgresql:5432/stayledger'
$runtimeDbUsername = 'stayledger'

kubectl --namespace stayledger create secret generic stayledger-runtime `
  --from-literal=postgres-password="$env:POSTGRES_PASSWORD" `
  --from-literal=password="$env:DB_PASSWORD" `
  --from-literal=DB_URL="$runtimeDbUrl" `
  --from-literal=DB_USERNAME="$runtimeDbUsername" `
  --from-literal=DB_PASSWORD="$env:DB_PASSWORD" `
  --dry-run=client -o yaml | kubectl apply -f -
```

Do not print, commit, or add the Secret values to a values file. Verify only
the key names:

```powershell
kubectl --namespace stayledger describe secret stayledger-runtime
```

## Render and install PostgreSQL

Render the pinned chart before applying it:

```powershell
helm template stayledger oci://registry-1.docker.io/bitnamicharts/postgresql `
  --version 18.7.12 `
  --namespace stayledger `
  --values deploy/helm/postgresql/values-local.yaml
```

Install or upgrade after the namespace and Secret exist:

```powershell
helm upgrade --install stayledger oci://registry-1.docker.io/bitnamicharts/postgresql `
  --version 18.7.12 `
  --namespace stayledger `
  --values deploy/helm/postgresql/values-local.yaml

kubectl rollout status statefulset/stayledger-postgresql `
  --namespace stayledger `
  --timeout=180s
kubectl get pods,pvc,svc --namespace stayledger
```

The PVC must report `Bound` before the database is considered ready. Inspect a
failed rollout with:

```powershell
kubectl get events --namespace stayledger --sort-by=.lastTimestamp
kubectl describe pod --namespace stayledger -l app.kubernetes.io/instance=stayledger
kubectl logs --namespace stayledger statefulset/stayledger-postgresql
```

To verify an authenticated local connection without exposing a password on the
client host, run the client inside the PostgreSQL Pod:

```powershell
kubectl exec --namespace stayledger statefulset/stayledger-postgresql -- `
  sh -ec 'PGPASSWORD="$(cat "$POSTGRES_PASSWORD_FILE")" psql --host 127.0.0.1 --username stayledger --dbname stayledger --command "SELECT 1;"'
```

## Deploy and verify StayLedger

The existing application chart uses the same Secret and does not create it.
Render both charts to confirm that only `secretKeyRef` values appear:

```powershell
helm lint deploy/helm/stayledger --values deploy/helm/stayledger/values-local.yaml
helm template stayledger deploy/helm/stayledger `
  --namespace stayledger `
  --values deploy/helm/stayledger/values-local.yaml
```

After the application image is available to Minikube, deploy it and wait for a
successful rollout:

```powershell
helm upgrade --install stayledger-app deploy/helm/stayledger `
  --namespace stayledger `
  --values deploy/helm/stayledger/values-local.yaml

kubectl rollout status deployment/stayledger-app-stayledger --namespace stayledger --timeout=180s
kubectl get deployment stayledger-app-stayledger --namespace stayledger -o yaml
```

If a release upgrade fails, inspect its history and roll back the affected
release without deleting the database PVC:

```powershell
helm history stayledger --namespace stayledger
helm rollback stayledger <revision> --namespace stayledger
helm history stayledger-app --namespace stayledger
helm rollback stayledger-app <revision> --namespace stayledger
```

Changing a credential after the database first initializes requires Bitnami's
documented password-update process or a deliberate fresh database. Do not
assume updating the Kubernetes Secret changes credentials stored in an existing
PVC.

## Cleanup and intentional data removal

Normal cleanup removes workloads and releases but retains the PostgreSQL PVC:

```powershell
helm uninstall stayledger-app --namespace stayledger
helm uninstall stayledger --namespace stayledger
kubectl get pvc --namespace stayledger
```

### Destructive: remove PostgreSQL data

This procedure permanently removes local database data. Run it only when a
fresh database is intended and after checking the exact claim name:

```powershell
kubectl get pvc --namespace stayledger
kubectl delete pvc <postgresql-pvc-name> --namespace stayledger
```

The deleted PVC data cannot be recovered by Helm rollback or reinstall.
