# StayLedger — Project Architecture

StayLedger follows a **DDD (Domain-Driven Design)** approach. The codebase is a
modular monolith split into three module groups: `core_*`, `infra_*`, and `ms_*`.

## Application diagram

```
┌─ ms_* ─────────────────────────────────────────────────────────┐
│ ms_app — Spring Boot application entry point                   │
│ application.yaml  ·  application-local.yaml                    │
│ src/test/resources/e2e  (happy path, end of mini-scenario)     │
└────────────────────────────────────────────────────────────────┘
      │  Telegram webhook in        ...In / ...Out out
┌─ infra_* ──────────────────────────────────────────────────────┐
│ telegram_impl  ·  ai_impl  ·  postgres_impl  ·  metric_impl    │
└────────────────────────────────────────────────────────────────┘
      │  ports: ...In / ...Out
┌─ core_* ───────────────────────────────────────────────────────┐
│ core_api — ...In / ...Out ports, DTOs, events                  │
│ core_impl — use cases, AggregateRoot (domain logic)            │
└────────────────────────────────────────────────────────────────┘
      │  Spring Events
      ▼
    other mini-scenarios
```

A mini-scenario is implemented as its **core** part (`core_api` + `core_impl`) plus one or more **infra** adapters; mini-scenarios communicate with each other via **Spring Events**.

## Module groups

### `core_*` — domain and application layer

- **`core_api`** — domain interfaces, DTOs, events.
  - Interfaces are split into two types: **IncomingPort** and **OutgoingPort**.
- **`core_impl`** — domain logic, use cases, entities (aggregate roots).

### `infra_*` — infrastructure adapters

- **`telegram_impl`** — Telegram Bot API integration.
- **`ai_impl`** — Spring AI / LLM integration.
- **`postgres_impl`** — persistence (JPA, repositories).
- **`metric_impl`** — metrics and observability.

### `ms_*` — application entry points (Spring Boot applications)

- **`ms_app`** — main application module:
  - `src/main/resources/application.yaml`
  - `src/main/resources/application-local.yaml`
  - `src/test/resources/e2e/` — end-to-end tests

## Development model: mini-scenarios

All development is driven by **mini-scenarios**. Each mini-scenario is implemented
as a **core** part (`core_api` + `core_impl`) plus one or more **infra** adapters
(`infra_*`). Every change is expected to map to a mini-scenario with its core and
infra implementation.

### Mini-scenario package documentation

Every mini-scenario must have a **`package-info.java`** at its **top-level package**.
Its Javadoc describes the specification the mini-scenario implements.

In the OpenSpec context, that specification is a **capability** — the `spec.md` file
for a specific area of the system's behavior, located at
`openspec/specs/<capability>/spec.md`. The Javadoc must point to the capability
(the spec) against which the mini-scenario is executed.

## Mini-scenario ports

Port naming and package conventions are described in
[docs/codestyle.md](codestyle.md).

### Flow of a mini-scenario

```
...In  (incoming port,   from infra_...port.incoming)
   ->  AggregateRoot     (core_impl, when working with the DB)
   ->  ...Out            (outgoing port, from infra_...port.outgoing)
```

- The **`AggregateRoot`** is passed **only** to `postgres_impl`.
- For a **`get...`** method, a **`Criteria`** may be passed instead.
- In either case, the object passed to the outgoing port must contain **all the data
  needed to retrieve or update** the information.

## Transport

Internal communication **between mini-scenarios** uses **Spring Events**.

## Testing

- **Mappers and factories** — covered by **unit tests**.
- **Ports** — covered by **integration tests**.
- **End-to-end (e2e) tests** — only the **happy path**, written **at the end of a
  mini-scenario**.
