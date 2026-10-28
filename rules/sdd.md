# Spec Driven Development (SDD)

This document describes the Spec Driven Development (SDD) process used by StayLedger.

## Source of truth

OpenSpec capability specifications under `openspec/specs/<capability>/spec.md` are the single source of truth for product behavior. Each mini-scenario maps 1:1 to a capability specification. See [rules/architecture.md](architecture.md) for the architecture and capability map.

This document defines the process for creating, reviewing, implementing, and maintaining those specifications; it does not replace the capability specifications.

## Package documentation

Each `package-info.java` Javadoc starts with the OpenSpec change name that created the package, followed by ` - ` and a short description. Use the change directory name from `openspec/changes/<change-name>/`.

## Change workflow

1. Use the OpenSpec `propose` workflow to create a change proposal, design, tasks, and specification deltas before implementation.
2. Review and agree on the planning artifacts before starting implementation with the OpenSpec `apply` workflow.
3. After implementation and verification, archive the completed change so its specification deltas are incorporated into the capability specifications.

Keep OpenSpec project context in `openspec/config.yaml`. Keep architecture and coding conventions in their project documentation and follow `AGENTS.md`.
