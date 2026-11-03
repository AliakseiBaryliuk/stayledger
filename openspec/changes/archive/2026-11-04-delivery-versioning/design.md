# Design

## Context

The root Gradle build already derives `project.version` from
`gradle.properties` and supports the `-PappVersion` override. The `_ms` module
is a Spring Boot application on port 8081, and the existing runtime capability
guarantees that it can start without database credentials. There are currently
no Docker, Nexus, or shared image-build assets.

## Goals / Non-Goals

**Goals:**

- Produce a version-consistent boot JAR and OCI image from one build input.
- Provide a local Nexus Docker endpoint with protected publication and
  anonymous local consumption.
- Make local build, push, and smoke verification reusable by a later Jenkins
  pipeline.

**Non-Goals:**

- Jenkins, merge queues, remote registry publication, Kubernetes deployment,
  TLS, and non-loopback registry access.
- Changing application HTTP or database behavior.

## Decisions

### Nexus Repository is the local registry

Run Nexus through a dedicated Compose file with persistent data and bind its UI
to `127.0.0.1:8082` and Docker endpoint to `127.0.0.1:5000`. A bootstrap tool
uses locally supplied environment credentials to create `stayledger-hosted`, a
publisher role, anonymous pull access, and an `ALLOW_ONCE` write policy.

This keeps Nexus credentials out of version control and makes the registry
closer to a production artifact manager than a bare Distribution container.
Harbor was considered for its built-in scanning, but Nexus also supports the
future Gradle/Maven repository use case.

### One version enters Gradle and Docker

The image-build command accepts an optional version override, passes it to
Gradle as `-PappVersion`, and passes the same value to Docker as a build
argument. Without an override, it reads the branch default. This prevents JAR
and image tags from diverging and gives Jenkins a single reusable entry point.

### Multi-stage, non-root runtime image

The Dockerfile builds the boot JAR in a Java 21 Gradle stage and copies only
the resulting versioned boot JAR into a Java 21 JRE runtime stage. The runtime
creates and uses an unprivileged application user, exposes 8081, and runs the
specific boot JAR rather than relying on a wildcard.

The runtime image intentionally does not contain build tools, source files,
Git metadata, or credentials. `.dockerignore` enforces the same boundary for
the build context.

### Smoke test relies on the existing database-free startup contract

The smoke command runs the built image without database variables and verifies
the health endpoint. It does not introduce a PostgreSQL Compose dependency,
because the runtime-observability capability already requires database-free
technical startup.

## Risks / Trade-offs

- [Local HTTP registry] → Bind both Nexus ports to loopback and document the
  Docker engine's local insecure-registry requirement when applicable.
- [Nexus credentials] → Supply bootstrap and publisher credentials through an
  ignored local environment file; never log or commit them.
- [Unavailable Docker daemon] → Keep Docker checks explicit and fail with a
  clear prerequisite message; the repository does not attempt to start Docker.
- [Mutable version input] → Enforce repository-side `ALLOW_ONCE` and validate
  the requested version before building or pushing.

## Migration Plan

1. Add the Compose, bootstrap, Docker, ignore, and build/smoke assets.
2. Start and bootstrap local Nexus with credentials supplied outside Git.
3. Build, smoke-test, authenticate, and push a versioned image.
4. Update Stage 2 instructions with the local workflow.
5. Roll back by stopping the Compose stack and removing the new local assets;
   no existing image, application, or database behavior is migrated.
