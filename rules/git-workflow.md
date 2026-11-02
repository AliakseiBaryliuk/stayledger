# StayLedger — Git workflow

The integration branch is `stayledger-codex` (`origin/stayledger-codex`). `master` and `origin/main` are legacy; do not target them.

## Integration branch only via pull request

- Never commit or push directly to `stayledger-codex`.
- Flow: branch off `stayledger-codex` -> commit(s) -> push the branch -> pull request -> merge.
- Branch naming: `<type>/<short-topic>` (`feature/booking-calendar`, `fix/...`, `chore/...`).
- Merge with **Rebase and merge** to keep a linear history; no merge commits into `stayledger-codex`.

## Commit messages

Every subject starts with a task tag, followed by a concise summary:

```
[<openspec-change-name>] <concise summary>
[NO_TASK] <concise summary>
[<task-number>] <concise summary>
```

- `[<openspec-change-name>]` — the change was carried out through OpenSpec. Use the change directory name from `openspec/changes/` (or its archived directory), for example `[initialize-project-structure]`.
- `[NO_TASK]` — the change was carried out directly, without an OpenSpec change, and has no tracker task id.
- `[<task-number>]` — the tracker id exactly as it is (`[1234]`, `[SL-42]`). It must match the task id recorded in the `package-info.java` of the mini-scenario the commit touches (see `rules/architecture.md`), so the tag and the code point at the same task. Never invent a number.
- Select the OpenSpec change tag first when the commit belongs to an OpenSpec change, even if a tracker id exists. Otherwise use the tracker id when one exists; use `[NO_TASK]` only when neither applies.
- Summary: short, imperative, to the point; no filler ("some fixes", "WIP"), no trailing period.
- Commit messages are written in English, like the rest of the repository.
- Optional body: why the change is needed. Keep it brief.

Examples:

```
[update-git-workflow] add OpenSpec commit tag rules
[NO_TASK] update project guidance directly
[1234] add git workflow rules
[1234] reject overlapping bookings
```

Commits made before this rule (`init app`, `define config`) stay as they are; new commits use the tag.

The tracked `hooks/commit-msg` hook checks the subject and requires the matching OpenSpec change tag when staged files belong to a change or the current `<type>/<change-name>` branch has an active change directory. Enable it in each clone with `git config core.hooksPath hooks`. Git does not install this repository hook automatically; a hook can also be bypassed with `--no-verify`.

## Before opening a pull request

- For OpenSpec work, archive the completed change and include the archive in the branch before opening a PR. Run `python scripts/check_openspec_archive.py --base stayledger-codex --head HEAD` after committing. If it names an unarchived change, stop and warn about the missing archive. Do not open the PR until it is archived.
- The `OpenSpec archive / archive` GitHub Actions check runs on PRs targeting `stayledger-codex`. Make that status check required in the branch protection or ruleset for `stayledger-codex` to prevent merging an unarchived change. GitHub Actions runs after PR creation, so repository automation cannot prevent the PR form from being submitted; the local preflight and this required check cover the two stages.
- Squash all commits added on the working branch since it branched from `stayledger-codex` into one commit before creating the pull request. Do not squash commits inherited from `stayledger-codex`.
- The squashed commit subject must follow the task-tag format above.

## Rebase before every push to remote

```bash
git fetch origin
git switch stayledger-codex
git rebase origin/stayledger-codex        # or: git pull --ff-only
git switch <my-branch>
git rebase stayledger-codex               # bring the integration branch into the working branch
# resolve conflicts, run the tests from rules/architecture.md
git push --force-with-lease     # never plain --force / -f
```

Repeat this cycle before **every** push, not just the first one. After the pull request is
merged, delete the branch and start the next one from a fresh `stayledger-codex`.

## Conflicts

- Resolve conflicts in the working branch; never rewrite or resolve inside `stayledger-codex`.
- Re-run tests before pushing: unit for mappers/factories, integration for ports, e2e happy path last.

## Local helpers (once per machine)

```bash
git config --global pull.rebase true
git config --global rerere.enabled true
git config --global branch.autoSetupRebase always
```
