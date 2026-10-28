# Design

## Context

The repository has project guidance and an OpenSpec root but no source modules or Gradle build. The proposal defines the scope. Existing architecture groups code into `_core`, `_infra`, and `_ms`; this scaffold creates only the currently requested PostgreSQL adapter.

## Goals / Non-Goals

**Goals:**

- Establish a buildable Kotlin DSL Gradle multi-project with Java 21 and Spring Boot 4.1.x.
- Keep `com.stayledger` as the root Java package and provide one minimal Spring Boot entry point.
- Preserve the existing documentation while moving it from `docs/` to `rules/`.
- Create empty module-local `AGENTS.md` files for the four Gradle projects.

**Non-Goals:**

- Implement mini-scenarios, ports, persistence behavior, migrations, or business APIs.
- Create Telegram, AI, or metric adapter projects.
- Provision a local PostgreSQL server with Docker Compose.

## Decisions

### Gradle project layout

Use one root Gradle build and four Java projects, with the architecture groups represented by directories:

```text
_core/core-api
_core/core-impl
_infra/postgres_adapter
_ms
```

Use four flat Gradle project IDs and map them to the architecture folders in `settings.gradle.kts`:

| Gradle project ID | Project directory |
|---|---|
| `:core-api` | `_core/core-api` |
| `:core-impl` | `_core/core-impl` |
| `:postgres_adapter` | `_infra/postgres_adapter` |
| `:_ms` | `_ms` |

This keeps `_core` and `_infra` as filesystem grouping directories, not Gradle projects. Give each of the four projects its own `build.gradle.kts` and empty root `AGENTS.md`.

### Toolchain and plugins

Use Kotlin DSL, the Gradle Wrapper 9.8.2, Java toolchains targeting 21, and Spring Boot 4.1.2 in `_ms`. These are compatible supported versions as of 2026-10-28. Keep shared Java configuration in the root build and apply the Spring Boot application plugin only to `_ms`.

### Packages and documentation

Use `com.stayledger` as the base package in every module, with no mini-scenario subpackages yet. Add a small package marker where needed so the empty source roots are tracked. Move every existing Markdown file from `docs/` to `rules/` without deleting documentation; update internal links and references from `AGENTS.md`, OpenSpec project/config context, and package examples to the new paths while retaining the existing package convention.

### PostgreSQL and application entry point

Keep only `_infra/postgres_adapter` under `_infra`. Add the PostgreSQL JDBC driver there and configure connection properties through environment variables; do not add Compose, JPA behavior, schema management, or credentials. Add a minimal `com.stayledger` Spring Boot application class in `_ms`, with no business logic.

### OpenSpec scope

This change does not alter product requirements. Set `skip_specs: true` and do not create a capability delta spec.

## Risks / Trade-offs

- The `_ms` application cannot connect to PostgreSQL until valid connection environment variables and an external database are provided.
- The existing architecture document describes adapters not included in this first scaffold; retain those references as future architecture, while creating only the PostgreSQL adapter project now.
- Existing package references must remain consistent with the `com.stayledger` base package when documentation paths are updated.

## Migration Plan

Move `docs/` to `rules/` with a rename-preserving operation, then update all references. Add the root Gradle build, wrapper, four project build files, module source roots, package markers, module-local empty `AGENTS.md` files, environment-based datasource properties, and the `_ms` entry point. Build and inspect the project tree before completing the change.

## Open Questions

None.
