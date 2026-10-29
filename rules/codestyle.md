# StayLedger — Code Style & Conventions

## General conventions

- Keep **DTOs separated from Entities** (mapping via **MapStruct** or a factory).
- All external calls (Telegram, LLM) go through **Resilience4j**.

### Types: records vs Lombok

- Use a **`record`** for immutable data carriers: DTOs, value objects, commands,
  requests, criteria, and events. Do **not** put Lombok `@Data` / `@Builder` on
  records.
- Use **Lombok** (`@Data`, `@Builder(toBuilder = true)`) only on **mutable** types
  that need it (typically JPA entities). Always add `@Builder(toBuilder = true)`
  when `@Builder` is used.

## Records

- Always add a **Javadoc** above the `record`.
- Document **every** record component with a `@param` tag, placed above the record
  (inside the same Javadoc as the record).

Example:

```java
/**
 * Immutable carrier of the data returned by the mini-scenario.
 *
 * @param a the first value
 * @param b the second value
 */
public record Data(
    @Nullable Object a,
    @Nonnull Object b
) {}
```

### Annotation layout in records

- With a **single** annotation, place it on the **same line** as the field, and do
  **not** put blank lines between fields:

```java
public record Data(
    @Nullable Object a,
    @Nonnull Object b
) {}
```

- With **two or more** annotations, place each annotation on its **own line above**
  the field, and separate the components with blank lines:

```java
public record Data(
    @Nullable Object a,

    @Nonnull
    @NotBlank
    String b,

    @Nullable Object c,
    @Nullable Object d,
) {}
```

### Field order in records

Components are ordered **top to bottom**:

1. primitives
2. objects
3. arrays
4. lists, sets, maps

## Nullability annotations

Use **Jakarta** nullability annotations only:

- `jakarta.annotation.Nonnull` — non-null
- `jakarta.annotation.Nullable` — nullable

Do not mix in JetBrains, Lombok, or Spring `@NonNull` / `@NotNull`.

- Annotate **every field, method parameter, and method return value**.
- For a method's **return value**, write the annotation on its own line **above**
  the method (not on the return type).

Example:

```java
@Nonnull
public String get(
    @Nonnull Object a,
    @Nonnull Object b,
    @Nullable Object c
) {

}
```

## Method argument formatting

- If a method has **more than 2 arguments**, place each argument on its own line.
- If a method has **2 or fewer arguments**, keep them on a single line.

Example (method with more than 2 arguments):

```java
@Nonnull
public String get(
    @Nonnull Object a,
    @Nonnull Object b,
    @Nullable Object c
) {

}
```

## Ports and naming convention

Ports are the domain interfaces of a mini-scenario. The naming rules are:

- **Core API incoming interfaces** live under
  `com.stayledger.<mini-scenario>.<state>.port.incoming` and are named
  `<UseCase>IncomingPort`.
- **Core API outgoing interfaces** live under
  `com.stayledger.<mini-scenario>.<state>.port.outgoing` and are named
  `<UseCase>OutgoingPort`.
- A database outgoing interface is named `<UseCase>ReadOnlyOutgoingPort` for a
  read-only operation or `<UseCase>WriteOnlyOutgoingPort` for a write operation.
  Do not use an unqualified `<UseCase>OutgoingPort` for a database operation.
- **Core Impl incoming-port implementations** live under
  `com.stayledger.application.<mini-scenario>.<state>.port.incoming` and are
  named `<UseCase>IncomingPort`. They implement the matching Core API incoming
  interface.
- An incoming port accepts a **command or request**, never a Spring Event. Events
  are inter-scenario transport only; see [rules/architecture.md](architecture.md).
- Always add a **Javadoc** to every port interface.

## Mappings and naming convention

- If the fields map **one-to-one**, or with **up to 3**
  `@Mapping(target = ..., source = ...)` / `@Mapping(target = ..., constant = ...)`,
  create a **MapStruct mapper** with the method:

  ```java
  B map(A a, ...);
  ```

  - Name: **`AToBMapper`**.
  - Package: `com.stayledger.application.<mini-scenario>.<state>.mapper`.

- If the mapping is **complex**, create a **factory** instead, with the method:

  ```java
  B create(A a, ...);
  ```

  - Name: **`BFactory`**.
  - Package: `com.stayledger.application.<mini-scenario>.<state>.factory`.
