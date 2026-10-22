# StayLedger — Git workflow

The integration branch is `master` (`origin/master`). `origin/main` is legacy; do not target it.

## Master only via pull request

- Never commit or push directly to `master`.
- Flow: branch off `master` -> commit(s) -> push the branch -> pull request -> merge.
- Branch naming: `<type>/<short-topic>` (`feature/booking-calendar`, `fix/...`, `chore/...`).
- Merge with **Rebase and merge** to keep a linear history; no merge commits into `master`.

## Commit messages

Every subject starts with a task tag, followed by a concise summary:

```
[NO_TASK] <concise summary>
[<task-number>] <concise summary>
```

- `[NO_TASK]` — no tracker task for this change (for example, work that exists only as an OpenSpec change, or a mini-scenario whose `package-info.java` records no task id).
- `[<task-number>]` — the tracker id exactly as it is (`[1234]`, `[SL-42]`). It must match the task id recorded in the `package-info.java` of the mini-scenario the commit touches (see `docs/architecture.md`), so the tag and the code point at the same task. Never invent a number.
- Summary: short, imperative, to the point; no filler ("some fixes", "WIP"), no trailing period.
- Commit messages are written in English, like the rest of the repository.
- Optional body: why the change is needed. Keep it brief.

Examples:

```
[NO_TASK] add git workflow rules
[NO_TASK] reject overlapping bookings
[1234] add git workflow rules
[1234] reject overlapping bookings
```

Commits made before this rule (`init app`, `define config`) stay as they are; new commits use the tag.

## Rebase before every push to remote

```bash
git fetch origin
git switch master
git rebase origin/master        # or: git pull --ff-only
git switch <my-branch>
git rebase master               # bring master into the working branch
# resolve conflicts, run the tests from docs/architecture.md
git push --force-with-lease     # never plain --force / -f
```

Repeat this cycle before **every** push, not just the first one. After the pull request is
merged, delete the branch and start the next one from a fresh `master`.

## Conflicts

- Resolve conflicts in the working branch; never rewrite or resolve inside `master`.
- Re-run tests before pushing: unit for mappers/factories, integration for ports, e2e happy path last.

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
- The current branch is not `master`
- Exactly 1 commit ahead of `origin/master` (squashed)
- The last commit subject matches `[<task-number>] <summary>` or `[NO_TASK] <summary>`

Bypass is possible with `--no-verify` (intentional override, not a default).
