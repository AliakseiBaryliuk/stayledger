# Design

## Context

See `proposal.md` for motivation and `specs/runtime-observability/spec.md` for the behavior contract. `_ms` currently has a minimal Spring Boot entry point, the basic starter, and PostgreSQL environment placeholders. No HTTP handler or tests exist. `postgres_adapter` contributes a driver but no persistence use case.

## Goals / Non-Goals

**Goals:** Keep technical runtime behavior in `_ms`, make process startup independent of PostgreSQL, and verify the HTTP contract against a running application.

**Non-Goals:** Add a business mini-scenario, persistence health check, or deployment routing in this stage.

## Decisions

### Technical HTTP interface

Add the Spring Boot 4 MVC starter to `_ms`. Implement GET `/internal/ping` as a small handler in a technical `_ms` package, with a `package-info.java` pointing at the `runtime-observability` capability. The handler does not call core modules. This exercises the real HTTP server; a static resource would make the technical contract less explicit, and a core port would invent business structure for a process check.

### Health and metrics

Add Actuator and the Micrometer Prometheus registry to `_ms`. Enable health availability probes and expose only `health` and `prometheus` through Actuator web exposure. Keep the standard paths from the delta spec on the application port. A separate management port would add deployment complexity before Kubernetes routing is designed. The later Helm and monitoring stages must route probes and scraping internally and exclude Actuator from external ingress.

### Database independence and ports

Keep the existing `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` placeholders. Do not add JDBC/JPA starters, migrations, repositories, or a database health contributor. Readiness therefore reflects process readiness in Stage 1; revisit its database semantics when persistence is introduced. Configure `server.port: 8081` in `_ms/src/main/resources/application.yaml` because 8080 is occupied locally. Integration tests still use a random port to avoid collisions; an explicit server port override remains available for other environments.

### Verification

Add an HTTP integration test that starts `_ms` on a random port and checks `/internal/ping`, overall health, liveness, readiness, Prometheus samples, and an unexposed Actuator endpoint. Run `./gradlew test` with Java 21, then launch the packaged application without database variables on its configured default port 8081 and probe the same paths. A handler-only unit test would not validate server startup or Actuator configuration.

## Risks / Trade-offs

- Readiness cannot represent future database availability. Mitigation: revisit the probe when the PostgreSQL stage introduces persistence behavior.
- Actuator shares the application port. Mitigation: expose only required endpoints now and restrict ingress paths in the later Helm stage.
- Port 8081 can be occupied in another environment. Mitigation: retain the standard server port override and use random ports in integration tests.

## Migration Plan

This stage adds technical endpoints without changing existing business behavior. Later deployment stages may adopt the paths after this version is released; a rollback removes those endpoints and requires probe configuration to roll back with the application.
