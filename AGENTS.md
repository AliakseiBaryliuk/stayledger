# StayLedger — Agent Instructions

Codex reads this file as the repository's project guidance. Read it before making changes.

## Project documentation

- `rules/architecture.md` — DDD, modular monolith, and mini-scenarios
- `rules/codestyle.md` — Java code style and conventions
- `rules/git-workflow.md` — branch, commit-message, and pull-request policy
- `rules/sdd.md` — Spec Driven Development principles

Specifications live in `openspec/specs/<capability>/spec.md` (OpenSpec). Each mini-scenario maps 1:1 to a capability spec; `package-info.java` must point at it. See `rules/sdd.md` for the specification workflow.

## Universal project rules

These rules apply to all files in the StayLedger project.

- Read the applicable project guidance in this file before making changes.
- Follow the existing code style and conventions of the project.
- Commit messages must start with a task tag: `[NO_TASK]` or `[<task-number>]`.
- Never commit directly to `master`; use branches and pull requests.
- OpenSpec capability specifications are the single source of truth for product behavior; follow `rules/sdd.md` for the SDD workflow.

## Architecture

Follow `rules/architecture.md` before changing structure, ports, or tests. Do not invent modules outside that document.

- Slice each mini-scenario as `core-api` + `core-impl` + only the adapters it needs (`_infra`). Wire the app in `_ms`.
- Incoming ports take a command/request. Spring Events are transport **between** mini-scenarios only, never an incoming-port argument.
- Pass `AggregateRoot` only to `postgres_adapter`. Other outgoing ports get complete DTOs or criteria.
- Map a mini-scenario 1:1 to `openspec/specs/<capability>/spec.md`. Point `package-info.java` at that spec.
- Tests: unit for mappers/factories, integration for ports, MockWebServer for Telegram HTTP, e2e happy path last in `_ms`.

## Git workflow

Follow `rules/git-workflow.md`. The integration branch is `stayledger-codex`.

- Never commit or push directly to `stayledger-codex`; land changes via a branch plus a pull request.
- Before every push: `git fetch`, update `stayledger-codex` from `origin/stayledger-codex`, rebase the working branch onto `stayledger-codex`, then push.
- After a rebase push use `--force-with-lease`; never `--force`/`-f`.
- Never rewrite `stayledger-codex`; resolve conflicts only in the working branch.
- Commit subjects start with a task tag plus a concise English summary: `[NO_TASK] <summary>` when there is no tracker task, `[<task-number>] <summary>` when there is one. Never invent a number.
- The `[<task-number>]` tag must match the task id recorded in the `package-info.java` of the mini-scenario the change touches; when that file records none, use `[NO_TASK]`.

## Java style (for `.java` files)

Follow `rules/codestyle.md` for examples and full rules. Do not mix other nullability annotations.

- Immutable carriers (DTO, VO, command/request, criteria, event) are `record`s. No Lombok `@Data`/`@Builder` on records.
- Lombok `@Data` and `@Builder(toBuilder = true)` only on mutable types that need them (typically JPA entities).
- Nullability: `jakarta.annotation.Nonnull` and `jakarta.annotation.Nullable` on every field, parameter, and return. Return annotation goes on its own line above the method.
- Ports: follow the module-specific packages and naming rules in `rules/codestyle.md`.
- MapStruct `AToBMapper.map` when mapping is 1:1 or at most three `@Mapping`s; otherwise `BFactory.create`.
- External calls (Telegram, LLM) go through Resilience4j.

## Spec Driven Development (SDD)

Before implementing new features or changing product behavior, follow the OpenSpec workflow described in `rules/sdd.md`. Capability specifications in `openspec/specs/` are the source of truth; update them through OpenSpec change artifacts. These SDD rules are contained in this section.
