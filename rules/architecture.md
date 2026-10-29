# StayLedger — Project Architecture

StayLedger follows a **DDD (Domain-Driven Design)** approach. The codebase is a
modular monolith split into three module groups: `_core`, `_infra`, and `_ms`.

Product behavior lives in OpenSpec capabilities under `openspec/specs/`. This
document describes structure and conventions only.

## Application diagram

```
┌─ _ms ──────────────────────────────────────────────────────────────────┐
│ Spring Boot application entry point                                    │
│ application.yaml  ·  application-local.yaml                            │
│ src/test/resources/e2e  (happy path, end of mini-scenario)             │
└────────────────────────────────────────────────────────────────────────┘
      │  Telegram webhook in        ...In / ...Out out
┌─ _infra ───────────────────────────────────────────────────────────────┐
│ telegram_adapter  ·  ai_adapter  ·  postgres_adapter  ·  metric_adapter│
└────────────────────────────────────────────────────────────────────────┘
      │  ports: ...In / ...Out
┌─ _core ────────────────────────────────────────────────────────────────┐
│ core-api — domain entities/AggregateRoot, ...In / ...Out ports, DTOs,  │
│             commands/requests, events                                  │
│ core-impl — use cases and application-service orchestration            │
└────────────────────────────────────────────────────────────────────────┘
      │  Spring Events (between mini-scenarios only)
      ▼
    other mini-scenarios
```

A mini-scenario is implemented as its **core** part (`core-api` + `core-impl`) plus one or more **infra** adapters; mini-scenarios communicate with each other via **Spring Events**.

## Module groups

### `_core` — domain and application layer

- **`core-api`** — domain entities and aggregate roots, domain interfaces,
  DTOs, commands/requests, and events used as inter-scenario transport. Its
  types are consumed by `core-impl` and by outgoing port contracts.
  - Interfaces are split into two types: **IncomingPort** and **OutgoingPort**.
- **`core-impl`** — use cases and application-service orchestration. It depends
  on `core-api` and implements incoming ports.

### `_infra` — infrastructure adapters

- **`telegram_adapter`** — Telegram Bot API integration.
- **`ai_adapter`** — Spring AI / LLM integration.
- **`postgres_adapter`** — persistence (JPA, repositories).
- **`metric_adapter`** — metrics and observability.

### `_ms` — top level (Spring Boot application)

- `src/main/resources/application.yaml`
- `src/main/resources/application-local.yaml`
- `src/test/resources/e2e/` — end-to-end tests

## Development model: mini-scenarios

All development is driven by **mini-scenarios**. Each mini-scenario is implemented
as a **core** part (`core-api` + `core-impl`) plus one or more **infra** adapters
(`_infra`). Every change is expected to map to a mini-scenario with its core and
infra implementation.

### Mini-scenario package documentation

Every mini-scenario must have a **`package-info.java`** at its **top-level package**.
Its Javadoc describes the specification the mini-scenario implements.

In the OpenSpec context, that specification is a **capability** — the `spec.md` file
for a specific area of the system's behavior, located at
`openspec/specs/<capability>/spec.md`. The Javadoc must point to the capability
(the spec) against which the mini-scenario is executed.

### Capability map

| Mini-scenario | Capability (`openspec/specs/<id>`) | Typical adapters |
|---|---|---|
| `telegram-order-intake` | `telegram-order-intake` | `telegram_adapter` |
| `ai-client-replies` | `ai-client-replies` | `ai_adapter` |
| `booking-calendar` | `booking-calendar` | `postgres_adapter` |
| `inventory` | `inventory` | `postgres_adapter` |
| `damage-and-prepayment` | `damage-and-prepayment` | `postgres_adapter` |

Keep capability ids aligned with mini-scenario names. Add a row when introducing a new capability.

## Mini-scenario ports

Port naming and package conventions are described in
[rules/codestyle.md](codestyle.md).

An **incoming port** (`...In`) is called by an adapter (or another application
service). It accepts a **command or request** type, not a Spring Event. An
**outgoing port** (`...Out`) is implemented by an adapter.

**Spring Events** are only the transport **between** mini-scenarios. Do not use a
Spring Event as the argument of an incoming port. A listener in the receiving
mini-scenario maps the event into that mini-scenario's command/request and then
calls `...In`.

### Flow of a mini-scenario

```
adapter / event listener
   ->  ...In command/request   (incoming port)
   ->  AggregateRoot           (core-api domain model, when working with the DB)
   ->  ...Out                  (outgoing port)
```

- The **`AggregateRoot`** is defined in `core-api` and is passed **only** to
  `postgres_adapter` through its outgoing port.
- For a **`get...`** method, a **`Criteria`** may be passed instead.
- In either case, the object passed to the outgoing port must contain **all the data
  needed to retrieve or update** the information.

## Transport

Internal communication **between mini-scenarios** uses **Spring Events**. Ports
stay inside a mini-scenario; events cross mini-scenario boundaries.

## Spring AI tool calling

Tool calling uses **distributed tool ownership**. Each mini-scenario owns its own
tools and exposes them as a `ToolCallbackProvider`. The `ai_adapter` only collects
those providers and wires them into the `ChatClient`. Every tool delegates to the
mini-scenario's `...In` port.

## Testing

- **Mappers and factories** — covered by **unit tests**.
- **Ports** — covered by **integration tests**.
- **Telegram HTTP** — covered with **MockWebServer**.
- **End-to-end (e2e) tests** — only the **happy path**, written **at the end of a
  mini-scenario**.
