# StayLedger — Git workflow

> This document is the Git workflow for the StayLedger project. It supplements
> [`.cline/rules/02-git-workflow.md`](../.cline/rules/02-git-workflow.md) and
> [`docs/architecture.md`](architecture.md); specifications live in
> `openspec/specs/<capability>/spec.md`.

The integration branch is `stayledger-cline` (`origin/stayledger-cline`). `origin/main` is legacy; do not target it.

## Branching

- Never commit or push directly to `stayledger-cline`.
- Flow: branch off `stayledger-cline` → commits → push branch → pull request → merge.
- Branch naming: `<type>/<short-topic>` (`feature/booking-calendar`, `fix/...`, `chore/...`).
- Each branch implements **one** task / mini-scenario.

## Commit messages

Every subject starts with a task tag, followed by a concise summary in English:

```
[NO_TASK] <concise summary>
[<task-number>] <concise summary>
```

- `[NO_TASK]` — no tracker task for this change (for example, work that exists only as an OpenSpec change, or a mini-scenario whose `package-info.java` records no task id).
- `[<task-number>]` — the tracker id exactly as it is (`[1234]`, `[SL-42]`). It must match the task id recorded in the `package-info.java` of the mini-scenario the commit touches (see [`docs/architecture.md`](architecture.md)). Never invent a number.
- Summary: short, imperative, to the point; no filler ("some fixes", "WIP"), no trailing period.
- Commit messages are written in English — like the rest of the repository.
- Optional body: why the change is needed. Keep it brief.

Examples tied to StayLedger mini-scenarios:

```
[NO_TASK] add git workflow rules
[NO_TASK] reject overlapping bookings
[1234] add booking-calendar core-api port
[SL-42] implement inventory postgres_adapter
```

Commits made before this rule (`init app`, `define config`) stay as they are; new commits use the tag.

## Squash before push

A branch may contain intermediate commits during development. Before pushing,
squash **only the new** commits of this branch (not commits already present in
`stayledger-cline`) into a single commit with a tag and description:

```
[<task-number>] <feature summary>
[NO_TASK] <feature summary>
```

Use `git rebase -i` or `git reset --soft` onto `stayledger-cline`, then commit once.

## Rebase before every push

```bash
git fetch origin
git switch stayledger-cline
git rebase origin/stayledger-cline        # or: git pull --ff-only
git switch <my-branch>
git rebase stayledger-cline               # bring stayledger-cline into the working branch
# resolve conflicts, run tests (see docs/architecture.md)
git push --force-with-lease     # never plain --force / -f
```

Repeat this cycle before **every** push, not just the first one. After the
pull request is merged, delete the branch and start the next one from a fresh
`stayledger-cline`.

## Conflicts

- Resolve conflicts in the working branch; never rewrite or resolve inside `stayledger-cline`.
- Before pushing, run tests: unit for mappers/factories, integration for ports, MockWebServer for Telegram HTTP, e2e happy path at the end of the mini-scenario.

## Local helpers (once per machine)

```bash
git config --global pull.rebase true
git config --global rerere.enabled true
git config --global branch.autoSetupRebase always
```

## Pre-push hook (recommended)

A versioned `hooks/pre-push` script enforces branch discipline automatically.
Install it once per clone:

```bash
git config core.hooksPath hooks
chmod +x hooks/pre-push   # on Windows: Git Bash or `attrib +R hooks/pre-push`
```

The hook checks:
- The current branch is not `stayledger-cline`
- Exactly 1 commit ahead of `origin/stayledger-cline` (squashed)
- The last commit subject matches `[<task-number>] <summary>` or `[NO_TASK] <summary>`
- There is an approved pull request (at least 1 approval)

Bypass is possible with `--no-verify` (intentional override, not a default).

## Tying to StayLedger mini-scenarios

Every commit must touch a concrete mini-scenario, implemented as
`core-api` + `core-impl` + adapters (`_infra`). Structure:

```
_core/src/main/java/com/stayledger/<mini-scenario>/
  <state>/
    port/incoming/   ...In
    port/outgoing/   ...Out
    mapper/          AToBMapper
    factory/         BFactory
_infra/src/main/java/com/stayledger/<mini-scenario>/
  <adapter>/
_ms/src/main/resources/
  application.yaml
```

`package-info.java` at the top-level package of the mini-scenario must point to
the OpenSpec specification: `openspec/specs/<capability>/spec.md`.

### Capability map (from `docs/architecture.md`)

| Mini-scenario | Capability (`openspec/specs/<id>`) | Typical adapters |
|---|---|---|
| `telegram-order-intake` | `telegram-order-intake` | `telegram_adapter` |
| `ai-client-replies` | `ai-client-replies` | `ai_adapter` |
| `booking-calendar` | `booking-calendar` | `postgres_adapter` |
| `inventory` | `inventory` | `postgres_adapter` |
| `damage-and-prepayment` | `damage-and-prepayment` | `postgres_adapter` |

When introducing a new mini-scenario, add a row to this table.
