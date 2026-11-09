# Tasks

## 1. Chart foundation

- [x] 1.1 Create the Helm v3 chart structure at `deploy/helm/stayledger` with
  chart metadata and reusable release-name and label helpers; verify Helm
  recognizes the chart with `helm show chart deploy/helm/stayledger`.
- [x] 1.2 Add portable `values.yaml` and a local values file for image
  coordinates, Secret key mapping, non-sensitive settings, resources, rollout,
  and probes; verify `helm lint` accepts the chart with the local values file.

## 2. Application workload templates

- [x] 2.1 Add the ConfigMap and Deployment templates with configurable image,
  non-sensitive `SERVER_PORT`, explicit external Secret key references,
  resource constraints, rolling updates, labels, and the required Actuator
  probes; verify `helm template` renders no Secret resource or credential value
  and targets port 8081 with the liveness and readiness paths.
- [x] 2.2 Add the ClusterIP Service template using the Deployment selector and
  application port mapping; verify its rendered selector matches the Deployment
  labels and forwards to container port 8081.

## 3. Operational validation and usage

- [x] 3.1 Add chart-local usage documentation for creating the external Secret
  outside Git and running `helm upgrade --install` in an application namespace;
  verify the documented command uses the local values file and no credential
  literal.
- [x] 3.2 Run `helm lint` and `helm template` with the local values file and
  inspect the rendered manifest to verify all OpenSpec scenarios: resources,
  configurable image, no passwords, Secret references, Service wiring,
  resources, rolling update, and health probes.
