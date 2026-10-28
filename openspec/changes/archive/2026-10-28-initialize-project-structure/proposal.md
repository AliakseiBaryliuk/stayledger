# Proposal

## Why

The repository currently contains project guidance but no Java or Gradle project skeleton. Establishing the agreed module layout and base package gives future mini-scenarios a consistent place to start without introducing business behavior.

## What Changes

- Move the existing documentation files from `docs/` to `rules/`, preserve their contents, and update repository and OpenSpec references.
- Keep the existing Java base package `com.stayledger` in the scaffold and project guidance.
- Add a Kotlin DSL Gradle multi-project build using Java 21 and Spring Boot 4.1.x.
- Create only the agreed modules: `_core/core-api`, `_core/core-impl`, `_infra/postgres_adapter`, and `_ms`; do not scaffold Telegram, AI, or metric adapters yet.
- Add a `com.stayledger` source root and an empty local `AGENTS.md` to each Gradle module. Add only a minimal Spring Boot entry point in `_ms`, with no business behavior.
- Add the PostgreSQL JDBC driver and environment-based connection settings; do not add Docker Compose or database schema/business persistence code.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None.

This is a repository bootstrap and documentation reorganization, not a product behavior change. The change opts out of spec deltas with `skip_specs: true`.

## Impact

Affected areas are repository documentation paths and Java package conventions, Gradle settings/build scripts and wrapper, four module source roots and local agent guidance files, and the `_ms` bootstrap application. No product API or user-visible behavior changes.
