# Design

## Context

See `proposal.md` for motivation. There is no application code yet. Baseline product rules used to live only in OpenSpec `context`. This change records them as capabilities so later implementation can follow `docs/architecture.md` without inventing behavior.

## Goals / Non-Goals

**Goals:**

- One capability per mini-scenario, matching the capability map in `docs/architecture.md`.
- Delta specs that archive into `openspec/specs/<capability>/spec.md`.
- Keep implementation decisions out of specs; point later work at architecture and code style docs.

**Non-Goals:**

- Implementing `_core`, `_infra`, or `_ms` slices.
- Introducing ports, aggregates, or adapters in this change (none exist to reuse).
- Changing money or booking behavior beyond what the specs capture.

## Decisions

### Spec-only change, then archive

Archive merges ADDED requirements into main specs. That is how the project gets a durable baseline. Alternative: write `openspec/specs/` by hand and skip a change. Rejected because archive keeps Purpose + requirements in the OpenSpec lifecycle.

### Capability ids equal mini-scenario names

`docs/architecture.md` already maps five mini-scenarios to five spec ids. Alternative: nested domains (`orders/telegram-intake`). Rejected while the project uses a flat layout.

### Defer hexagonal slice to later changes

When a later change implements a capability, it follows the mini-scenario slice (`core-api` + `core-impl` + needed adapters only). `AggregateRoot` crosses only to `postgres_adapter`; other `Out` ports get complete DTOs or criteria. This seed does not add those types.

### Keep requirements thin

Only behaviors from the former core-logic list. Edge cases are limited to "missing/empty/failure" so specs stay testable without inventing pricing, overlap policy, or LLM fallback copy.

## Risks / Trade-offs

- [Thin specs leave later product questions open] → Next feature changes add ADDED/MODIFIED requirements instead of stuffing them here.
- [Archive before any code] → Specs describe intended behavior; apply/archive of feature changes must still confirm shipped behavior.

## Migration Plan

1. Complete planning artifacts for this change.
2. Archive `seed-baseline-specs` so main specs exist under `openspec/specs/`.
3. Implement each capability in later changes using the architecture slice; no rollback of product behavior because nothing ships in runtime.

## Open Questions

None. Overlap policy, damage exceeding prepayment, and LLM fallback wording are deferred to future spec changes.
