# Proposal

## Why

The `_ms` application has no HTTP server or runtime endpoints, so it cannot currently be checked locally or used by the planned Kubernetes probes and Prometheus scraper. This stage establishes that technical contract before deployment work begins.

## What Changes

- Make `_ms` a runnable HTTP application and add a minimal technical endpoint without business behavior.
- Provide overall health, liveness, readiness, and Prometheus metrics endpoints with limited Actuator web exposure.
- Add automated checks for startup and these endpoints on Java 21.
- Keep the PostgreSQL configuration environment based without adding database access behavior.

## Capabilities

### New Capabilities

- `runtime-observability`: Technical HTTP availability, process health probes, and Prometheus runtime metrics.

### Modified Capabilities

None.

## Impact

The implementation will affect `_ms` dependencies, application configuration, a technical HTTP handler, and tests. Kubernetes resources, external ingress routing, business APIs, persistence code, and changes to `_core` or `_infra` are outside this change.
