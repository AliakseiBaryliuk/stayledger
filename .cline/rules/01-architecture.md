---
paths:
  - "**/*"
---
# Architecture

Follow `docs/architecture.md` before changing structure, ports, or tests. Do not invent modules outside that document.

- Slice each mini-scenario as `core-api` + `core-impl` + only the adapters it needs (`_infra`). Wire the app in `_ms`.
- Incoming ports (`...In`) take a command/request. Spring Events are transport **between** mini-scenarios only, never the `...In` argument.
- Pass `AggregateRoot` only to `postgres_adapter`. Other `...Out` ports get complete DTOs or criteria.
- Map a mini-scenario 1:1 to `openspec/specs/<capability>/spec.md`. Point `package-info.java` at that spec.
- Tests: unit for mappers/factories, integration for ports, MockWebServer for Telegram HTTP, e2e happy path last in `_ms`.