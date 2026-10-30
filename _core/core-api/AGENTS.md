# Core API Module Instructions

This file supplements the repository-level `AGENTS.md`. Read and follow
`rules/architecture.md`, [rules/codestyle.md](../../rules/codestyle.md), and
`rules/sdd.md` before changing this module.

## Module Boundary

`core-api` contains the public contracts and domain model of mini-scenarios:
immutable transport types, port interfaces, entities, and aggregate roots. It
contains no use-case implementation, Spring configuration, controller, adapter,
repository, mapper, factory, or persistence-specific JPA implementation.

## Package Layout and Ownership

Use the lowercase base package `com.stayledger`.

```text
com.stayledger
├── shared
│   ├── constant
│   └── exception
└── <capability>
    └── <state>
        ├── entity
        ├── dto
        └── port
            ├── incoming
            └── outgoing
```

- `<capability>` is the mini-scenario identifier and must exactly match the
  capability directory name in `openspec/specs/<capability>/`.
- Each mini-scenario has `package-info.java` at
  `com.stayledger.<capability>`. Its Javadoc links to that capability's
  `spec.md`, as required by `rules/architecture.md`.
- `<state>` is used when a mini-scenario's state separation is needed; do not
  create arbitrary package layers. Port packages follow the mandatory layout
  `com.stayledger.<capability>.<state>.port.incoming|outgoing`.
- `dto` contains immutable API carriers, including DTOs, commands, requests, and
  criteria. Use `record` whenever possible.
- `entity` contains the mini-scenario's domain entities, including aggregate
  roots and their domain invariants. These are domain types, not JPA persistence
  entities; persistence mapping remains in `postgres_adapter`.
- `shared` is reserved for genuinely cross-mini-scenario API data. Put shared
  constants in `shared.constant` and shared exception types in
  `shared.exception`. Do not place mini-scenario-specific types in `shared`.
- Do not create implementation, adapter, persistence, or framework packages in
  this module.

## Ports

- `port.incoming` and `port.outgoing` contain interfaces only, with no
  implementation classes.
- Incoming interfaces are named `<UseCase>IncomingPort`; standard outgoing
  interfaces are named `<UseCase>OutgoingPort`. Database outgoing interfaces use
  `<UseCase>ReadOnlyOutgoingPort` or `<UseCase>WriteOnlyOutgoingPort` according
  to the operation. The authoritative package and naming rules are in
  [rules/codestyle.md](../../rules/codestyle.md).
- Incoming ports receive a command or request. They are called by an adapter,
  event listener, or application service; a Spring Event is never an
  incoming-port argument.
- Spring Events are inter-mini-scenario transport only. A receiving listener
  maps an event to its own command or request before invoking its incoming port.
- Every port interface has Javadoc describing its responsibility. Every method
  has Javadoc with `@param` and `@return` tags where applicable, describing the
  input and output contract.

## API Type and Style Rules

- Use `jakarta.annotation.Nonnull` or `jakarta.annotation.Nullable` on every
  record component, interface method parameter, and interface method return. Put
  the return annotation on its own line above the method.
- Document every record and each of its components with `@param` tags.
- Apply the record component order, annotation layout, method argument layout,
  and mapper/factory naming rules from `rules/codestyle.md`.
- Do not use Lombok `@Data` or `@Builder` on records. Mutable types are not part
  of this module.
- Do not introduce a dependency on Spring, an infrastructure adapter, or another
  mini-scenario package. Jakarta nullability annotations are allowed.

## Architecture Tests

Keep ArchUnit boundary tests under `src/test/java/com/stayledger`. They must
verify every production package `com.stayledger.<capability>..` depends only on:

- types in the same `<capability>` package;
- `com.stayledger.shared..`;
- Java platform and Jakarta annotation types.

The tests must reject direct dependencies from one mini-scenario package to
another. Add or update the relevant ArchUnit test whenever a package boundary
is introduced or changed.
