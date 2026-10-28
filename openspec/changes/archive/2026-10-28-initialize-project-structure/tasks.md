# Tasks

## 1. Move and align project guidance

- [x] 1.1 Move all existing Markdown files from `docs/` to `rules/` without losing content, update every repository/OpenSpec/internal-link reference, and verify no active references point to `docs/`.
- [x] 1.2 Preserve Java package examples and root agent guidance using `com.stayledger`, then verify package conventions remain consistent after moving the documentation.

## 2. Add the Gradle multi-project skeleton

- [x] 2.1 Add the Gradle 9.8.2 wrapper, Kotlin DSL root build and settings with flat project IDs `:core-api`, `:core-impl`, `:postgres_adapter`, and `:_ms` mapped to the agreed directories; configure Java 21 and Spring Boot 4.1.2, then verify `./gradlew projects` lists exactly these four projects and no `_core` or `_infra` group projects.
- [x] 2.2 Add each module's build file, empty local `AGENTS.md`, and tracked `com/stayledger` source root; add only the PostgreSQL JDBC driver and environment-based datasource properties, then verify each requested directory and file exists.
- [x] 2.3 Add the minimal `com.stayledger` Spring Boot entry point in `_ms` without business behavior, then verify `./gradlew build` and `./gradlew :_ms:bootJar` succeed.
