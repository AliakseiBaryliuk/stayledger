# StayLedger — agent entry

This project uses **OpenSpec** (schema `spec-driven`). Planning and apply follow `openspec/config.yaml`; do not copy that context into artifacts.

## Workflows

Use the project skills/commands in `.cursor/skills` and `.cursor/commands`:

- `/opsx-explore` — think through a change; do not implement
- `/opsx-propose` — create planning artifacts only
- `/opsx-apply` — implement tasks from a change (each task ends in a commit; see `docs/git-workflow.md` for branch, PR, and rebase rules)
- `/opsx-sync` — merge delta specs into `openspec/specs/`
- `/opsx-archive` — archive a completed change
- `/opsx-update` — revise an in-flight change

Product behavior lives in `openspec/specs/` (and change deltas under `openspec/changes/`). Structure is in `docs/architecture.md`. Java form is in `docs/codestyle.md`.
