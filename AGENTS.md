# StayLedger — Agent Instructions

This repository uses Cline rules stored in `.cline/rules/`. Read them before making changes.

## Rule files

- `.cline/rules/00-universal.md` — always-active project rules
- `.cline/rules/01-architecture.md` — modular monolith and mini-scenario architecture
- `.cline/rules/02-git-workflow.md` — branch, commit-message, pull-request policy
- `.cline/rules/03-java-style.md` — Java naming, records, nullability (`.java` files)
- `.cline/rules/04-sdd.md` — Spec Driven Development rules

## Documentation

- `docs/architecture.md` — DDD, modular monolith, mini-scenarios
- `docs/codestyle.md` — Java code style and conventions
- `docs/git-workflow.md` — Git workflow and commit message format
- `docs/sdd.md` — Spec Driven Development principles

## Specification

Specifications live in `openspec/specs/<capability>/spec.md` (OpenSpec).
Each mini-scenario maps 1:1 to a capability spec; `package-info.java` must point at it.