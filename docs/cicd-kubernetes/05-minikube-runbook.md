# Stage 5 — Minikube Runbook

This runbook deploys the locally built StayLedger image and PostgreSQL to a
single local Minikube profile. It is the manual baseline for the later
[Jenkins pipeline](06-jenkins-pipeline.md); it does not automate Jenkins or
install Prometheus/Grafana from the [monitoring stage](07-monitoring.md).

## Supported boundary

- The operator has Docker, Minikube, `kubectl`, and Helm 3 installed and can
  start a Minikube driver supported on the local machine.
- The runbook uses a `stayledger` Minikube profile, namespace, PostgreSQL
  release, and database Service. It requires a dynamic StorageClass that can
  bind a ReadWriteOnce PVC.
- Nexus is a local source of immutable image coordinates, not an endpoint that
  Minikube must reach. `localhost:5000` on a Minikube node refers to that node,
  not the host's loopback Nexus registry.
- The application is reachable for a smoke check only through `kubectl
  port-forward`; no ingress or externally reachable Kubernetes Service is
  configured.

## 1. Prerequisites and cluster startup

Start Docker Desktop or the Docker engine, then verify the tools that the
runbook invokes:

```powershell
docker version
minikube version
kubectl version --client
helm version
```

Start a dedicated profile. Minikube selects the configured local driver; if the
machine needs a specific supported driver, pass it explicitly (for example,
`--driver=docker`) and use that same driver for the profile lifecycle.

```powershell
minikube start --profile stayledger
minikube status --profile stayledger
kubectl config use-context stayledger
kubectl config current-context
kubectl cluster-info
```

The current context must be `stayledger` before continuing. Create the
application namespace and verify that the cluster can dynamically provision
the persistent ReadWriteOnce volume required by PostgreSQL:

```powershell
kubectl create namespace stayledger --dry-run=client -o yaml | kubectl apply -f -
kubectl get storageclass
kubectl get storageclass -o custom-columns=NAME:.metadata.name,DEFAULT:.metadata.annotations.storageclass\.kubernetes\.io/is-default-class,PROVISIONER:.provisioner
```

Stop here if there is no compatible default StorageClass. Select a compatible
Minikube driver or pass the chosen class to the PostgreSQL chart as described
in the [PostgreSQL release guide](../../deploy/helm/postgresql/README.md).

## 2. Prepare and load the exact application image

Nexus gives the image a stable local coordinate; Minikube needs a separate
copy in its node image cache. Build or pull the exact version with the Stage 2
[delivery guide](02-versioning-and-docker.md), then use one set of variables
for every following command:

```powershell
$imageRepository = 'localhost:5000/stayledger'
$imageTag = '0.2.0-SNAPSHOT' # Replace with the exact built version.
$image = "${imageRepository}:$imageTag"

docker image inspect $image
minikube image load $image --profile stayledger
minikube image ls --profile stayledger | Select-String -SimpleMatch $image
```

`docker image inspect` and `minikube image ls` must both show the same image
coordinate. Do not replace `minikube image load` with `minikube docker-env` or
an in-cluster pull from `localhost:5000`: neither assumption is portable
across drivers or to the later Jenkins environment.

## 3. Create runtime configuration

The releases share an externally managed Secret. Choose `POSTGRES_PASSWORD`
and `DB_PASSWORD` through a secure local workflow; do not add their values to
Git or Helm values. The following check prevents accidentally creating a
Secret with empty passwords:

```powershell
if ([string]::IsNullOrWhiteSpace($env:POSTGRES_PASSWORD) -or
    [string]::IsNullOrWhiteSpace($env:DB_PASSWORD)) {
  throw 'Set POSTGRES_PASSWORD and DB_PASSWORD in the current shell first.'
}

$runtimeDbUrl = 'jdbc:postgresql://stayledger-postgresql:5432/stayledger'
$runtimeDbUsername = 'stayledger'

kubectl --namespace stayledger create secret generic stayledger-runtime `
  --from-literal=postgres-password="$env:POSTGRES_PASSWORD" `
  --from-literal=password="$env:DB_PASSWORD" `
  --from-literal=DB_URL="$runtimeDbUrl" `
  --from-literal=DB_USERNAME="$runtimeDbUsername" `
  --from-literal=DB_PASSWORD="$env:DB_PASSWORD" `
  --dry-run=client -o yaml | kubectl apply -f -

kubectl --namespace stayledger describe secret stayledger-runtime
```

`describe` must show the five key names, not their values. See the
[PostgreSQL release guide](../../deploy/helm/postgresql/README.md#runtime-secret)
for the Secret contract and credential-change constraint after initial
database creation.

## 4. Install PostgreSQL and wait for persistent readiness

Install the pinned chart only after the namespace, StorageClass preflight, and
Secret are complete:

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

The PostgreSQL Pod must be ready and its PVC must be `Bound` before installing
the application. The database is reached in-cluster through
`stayledger-postgresql:5432`, never through `localhost`.

## 5. Install StayLedger and verify rollout

Render the existing chart with the exact image coordinate, then install or
upgrade it. Passing the same variables used by image loading prevents the
release from selecting a different tag.

```powershell
helm lint deploy/helm/stayledger --values deploy/helm/stayledger/values-local.yaml
helm template stayledger-app deploy/helm/stayledger `
  --namespace stayledger `
  --values deploy/helm/stayledger/values-local.yaml `
  --set-string image.repository=$imageRepository `
  --set-string image.tag=$imageTag

helm upgrade --install stayledger-app deploy/helm/stayledger `
  --namespace stayledger `
  --values deploy/helm/stayledger/values-local.yaml `
  --set-string image.repository=$imageRepository `
  --set-string image.tag=$imageTag

kubectl rollout status deployment/stayledger-app-stayledger `
  --namespace stayledger `
  --timeout=180s
kubectl get deployment stayledger-app-stayledger --namespace stayledger
```

## 6. Smoke check through the Service

In one PowerShell window, run the foreground port-forward. Leave it running
only for the check and stop it with `Ctrl+C` afterwards:

```powershell
kubectl port-forward --namespace stayledger service/stayledger-app-stayledger 8081:8081
```

In another PowerShell window, confirm the readiness response:

```powershell
Invoke-WebRequest http://localhost:8081/actuator/health/readiness
```

An HTTP 200 response proves that the local client can reach the ClusterIP
Service and the application readiness endpoint.

## 7. Diagnose failures

Use the commands below before changing chart values or deleting workloads.

### Image unavailable or `ImagePullBackOff`

```powershell
docker image inspect $image
minikube image ls --profile stayledger | Select-String -SimpleMatch $image
kubectl get pods --namespace stayledger
kubectl describe pod --namespace stayledger -l app.kubernetes.io/instance=stayledger-app
```

If the node cache does not list the exact image, rerun `minikube image load`
with the same `$image` value, then restart the failed application rollout.

### Workload, Service, or readiness failure

```powershell
kubectl get pods,deployment,service --namespace stayledger
kubectl get events --namespace stayledger --sort-by=.lastTimestamp
kubectl describe deployment stayledger-app-stayledger --namespace stayledger
kubectl logs --namespace stayledger deployment/stayledger-app-stayledger
kubectl get endpoints stayledger-app-stayledger --namespace stayledger
```

### PostgreSQL readiness or connection failure

```powershell
kubectl describe pod --namespace stayledger -l app.kubernetes.io/instance=stayledger
kubectl logs --namespace stayledger statefulset/stayledger-postgresql
kubectl get pvc,service --namespace stayledger
kubectl exec --namespace stayledger statefulset/stayledger-postgresql -- `
  sh -ec 'PGPASSWORD="$(cat "$POSTGRES_PASSWORD_FILE")" psql --host 127.0.0.1 --username stayledger --dbname stayledger --command "SELECT 1;"'
```

The database check reads the password inside the Pod and does not expose it on
the client host.

## 8. Roll back and clean up safely

Inspect the relevant release history before rolling back only the failed
release:

```powershell
helm history stayledger --namespace stayledger
helm rollback stayledger <revision> --namespace stayledger
helm history stayledger-app --namespace stayledger
helm rollback stayledger-app <revision> --namespace stayledger
```

Normal cleanup removes workloads but retains database data:

```powershell
helm uninstall stayledger-app --namespace stayledger
helm uninstall stayledger --namespace stayledger
kubectl get pvc --namespace stayledger
```

### Destructive: remove PostgreSQL data

Delete a PVC only when a fresh database is intended. First inspect its exact
name; this action cannot be undone by Helm rollback or reinstall.

```powershell
kubectl get pvc --namespace stayledger
kubectl delete pvc <postgresql-pvc-name> --namespace stayledger
```

For chart-specific upgrades, credential rotation, and PVC behavior, use the
[PostgreSQL release guide](../../deploy/helm/postgresql/README.md).
