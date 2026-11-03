# StayLedger — Git workflow

`stayledger-codex` is the production branch. `stayledger-codex-develop`
(`origin/stayledger-codex-develop`) is the development integration branch.
`master` and `origin/main` are legacy; do not target them.

## Branches and pull requests

- Never commit or push directly to `stayledger-codex`, `stayledger-codex-develop`, or `release/RL-xx`.
- Normal flow: branch from `stayledger-codex-develop` -> commit(s) -> PR to `stayledger-codex-develop` -> merge.
- Normal branch naming is `<type>/<short-topic>` (`feature/booking-calendar`, `fix/...`, `chore/...`).
- A release starts by cutting `release/RL-xx` from a stable develop version. Release fixes branch from it as `fix/RL-xx/<short-topic>` and target that same release branch.
- `stayledger-codex-develop` never targets `stayledger-codex`. The final PR to production is only `release/RL-xx` -> `stayledger-codex`.
- Normal and release-fix PRs use **Rebase and merge**. The final release PR may use the repository-approved merge strategy because its production tag is created after the merge.

## Versions and release lifecycle

- `gradle.properties` is the branch-owned default version. `-PappVersion` overrides it for a specific build.
- A bootstrap or release cut advances develop to the next minor with a technical commit such as `version=0.3.0-SNAPSHOT` and an annotated `v0.3.0` marker tag. Marker tags do not publish artifacts or deploy.
- A working branch builds the next patch SNAPSHOT of its target line. A merge queue for `stayledger-codex-develop` and each `release/RL-xx` serializes merges, creates the technical patch version commit, then creates its annotated `vX.Y.Z` tag and immutable non-production artifacts.
- Every release-branch merge creates an automatic `release/RL-xx` -> `stayledger-codex-develop` sync PR. It preserves develop's `gradle.properties`; unresolved functional conflicts block the final release.
- After all release sync PRs merge and testing passes, the final release PR builds with `-PappVersion=X.Y.Z-RELEASE`, deploys that exact production artifact, then creates `vX.Y.Z-RELEASE`. The release branch then closes.

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

The tracked `hooks/commit-msg` hook checks the subject and requires the matching OpenSpec change tag when staged files belong to a change or the current `<type>/<change-name>` branch has an active change directory. Enable it in each clone with `git config core.hooksPath hooks`. Git does not install this repository hook automatically; it can be bypassed with `--no-verify`.

## Before opening a pull request

- When creating a PR for OpenSpec work, run `python scripts/check_openspec_archive.py --base <pr-target> --head HEAD`. Use `stayledger-codex-develop` for normal PRs, the relevant `release/RL-xx` for release fixes, and `stayledger-codex` only for the final release PR. If it names an unarchived change, show the author a warning. The warning does not block PR creation.
- The PR template repeats this warning and provides commands for each PR target.
- Squash all commits added on the working branch since it branched from its PR target into one commit before creating the pull request. Do not squash commits inherited from that target.
- The squashed commit subject must follow the task-tag format above.

## Rebase before every push to remote

```bash
git fetch origin
git switch <pr-target>
git rebase origin/<pr-target>              # or: git pull --ff-only
git switch <my-branch>
git rebase <pr-target>                     # bring the target branch into the working branch
# resolve conflicts, run the tests from rules/architecture.md
git push --force-with-lease     # never plain --force / -f
```

Repeat this cycle before **every** push, not just the first one. After the pull request is
merged, delete the branch and start the next one from the appropriate target branch.

## Conflicts

- Resolve conflicts in the working branch; never rewrite or resolve inside an integration or release branch.
- Re-run tests before pushing: unit for mappers/factories, integration for ports, e2e happy path last.

## Local helpers (once per machine)

```bash
git config --global pull.rebase true
git config --global rerere.enabled true
git config --global branch.autoSetupRebase always
```
