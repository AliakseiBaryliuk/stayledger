# Tasks

## 1. Technical HTTP runtime

- [x] 1.1 Configure `_ms` to listen on port 8081 by default and verify `application.yaml` contains `server.port: 8081` while port 8081 is free locally.
- [x] 1.2 Add the Spring Boot 4 MVC starter to `_ms` and verify `:_ms:compileJava` succeeds with Java 21.
- [x] 1.3 Implement GET `/internal/ping` in a technical `_ms` package, document its `runtime-observability` capability in `package-info.java`, and verify an HTTP integration test receives 200 without invoking business modules.

## 2. Runtime observability

- [x] 2.1 Add Actuator and Micrometer Prometheus registry to `_ms`; enable availability probes and limit web exposure to `health` and `prometheus`, then verify the application configuration contains those settings.
- [x] 2.2 Add HTTP integration tests for overall health, liveness, readiness, Prometheus metric samples, and a non-exposed Actuator endpoint; verify they pass without database environment variables or a running PostgreSQL server.

## 3. Integration check

- [x] 3.1 Run `./gradlew test` with Java 21 and verify all modules pass; launch the packaged `_ms` application without database variables on default port 8081 and verify `/internal/ping` and the Actuator endpoints respond as specified.
