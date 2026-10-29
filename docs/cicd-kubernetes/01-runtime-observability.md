# Stage 1 — Application Runtime and Observability

**Proposed branch:** `feature/runtime-observability`  
**Dependencies:** none

## Objective

Make the `_ms` module a runnable HTTP application that can be checked locally and later probed by Kubernetes and Prometheus.

## Changes

- Add Spring MVC, Actuator, and Micrometer Prometheus Registry to `_ms` while retaining Java 21 and the current module structure.
- Add a minimal technical HTTP endpoint with no business logic and a test for its availability.
- Enable liveness and readiness health groups and `/actuator/prometheus`.
- Limit Actuator web exposure to technically required endpoints; do not expose them through an external ingress.
- Keep PostgreSQL settings in environment variables. Do not add JPA, migrations, or a data model until a mini-scenario requires database access.

## Out of Scope

- Business APIs and changes to `_core` or `_infra`.
- Kubernetes manifests, Docker, and the monitoring stack.

## Acceptance Criteria

- `./gradlew test` passes with Java 21.
- The application starts without business modules and responds on the technical HTTP endpoint.
- `/actuator/health`, readiness, and liveness return the expected healthy status.
- `/actuator/prometheus` is available and returns Prometheus-compatible metrics.
