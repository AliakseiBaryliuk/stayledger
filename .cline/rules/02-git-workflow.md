# Git workflow

Follow `docs/git-workflow.md`. The integration branch is `stayledger-codex`.

- Never commit or push directly to `stayledger-codex`; land changes via a branch plus a pull request.
- Before every push: `git fetch`, update `stayledger-codex` from `origin/stayledger-codex`, rebase the working branch onto `stayledger-codex`, then push.
- After a rebase push use `--force-with-lease`; never `--force`/`-f`.
- Never rewrite `stayledger-codex`; resolve conflicts only in the working branch.
- Commit subjects start with a task tag plus a concise English summary: `[NO_TASK] <summary>` when there is no tracker task, `[<task-number>] <summary>` when there is one. Never invent a number.
- The `[<task-number>]` tag must match the task id recorded in the `package-info.java` of the mini-scenario the change touches; when that file records none, use `[NO_TASK]`.
