# Core Impl Module Instructions

This file supplements the repository-level `AGENTS.md`. Read and follow
`rules/architecture.md`, [rules/codestyle.md](../../rules/codestyle.md), and
`rules/sdd.md` before changing this module.

## Module Boundary

`core-impl` depends on `core-api` and implements incoming ports through use
cases and application-service orchestration. Keep domain invariants in the
aggregate root. An aggregate root may be passed only to `postgres_adapter`; all
other outgoing port contracts receive complete DTOs or criteria, as defined in
`rules/architecture.md`.

## Package Layout and Ownership

Use the lowercase base package `com.stayledger`.

```text
com.stayledger
└── application
    ├── config
    └── <capability>
        └── <state>
            ├── factory
            ├── mapper
            └── port
                └── incoming
```

- `<capability>` is the mini-scenario identifier and must exactly match the
  capability directory name in `openspec/specs/<capability>/`.
- `<state>` is used when a mini-scenario's state separation is needed; do not
  create arbitrary package layers.
- `mapper` contains MapStruct mappers for simple mappings. `factory` contains
  factories for complex mappings. Create the package or packages required by
  the use case: use either a mapper or a factory, or both when the mappings
  require them.
- Incoming-port implementations are located in
  `com.stayledger.application.<capability>.<state>.port.incoming`.
- Spring configuration belongs in `com.stayledger.application.config`.

## Ports

- Incoming-port implementations perform business use cases through adapters.
- Incoming ports receive a command or request; a Spring Event is never an
  incoming-port argument. Spring Events are inter-mini-scenario transport only.
  A receiving listener maps an event to its own command or request before
  invoking its incoming port.

## Architecture Tests

Keep ArchUnit boundary tests under `src/test/java/com/stayledger`. They must
verify every production package
`com.stayledger.application.<capability>..` depends only on:

- types in the same application `<capability>` package;
- types in the matching `com.stayledger.<capability>..` Core API package;
- Java platform, Jakarta annotation, Spring, and mapping-library types.

The tests must reject direct dependencies between application packages of
different mini-scenarios and from an application mini-scenario to a Core API
package of a different mini-scenario. Add or update the relevant ArchUnit test
whenever an application package boundary is introduced or changed.
