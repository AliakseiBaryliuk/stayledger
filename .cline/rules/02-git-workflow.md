# Git workflow

Follow `docs/git-workflow.md`. The integration branch is `stayledger-cline`.

- When starting a new OpenSpec flow, create a new branch from `stayledger-cline` and work on it.
- Never commit or push directly to `stayledger-cline`; land changes via a branch plus a pull request.
- A pull request must be approved (at least 1 approval) before pushing to `stayledger-cline`.
- Commit subjects start with a task tag plus a concise English summary: `[NO_TASK] <summary>` when there is no tracker task, `[<task-number>] <summary>` when there is one. Never invent a number.
- The `[<task-number>]` tag must match the task id recorded in the `package-info.java` of the mini-scenario the change touches; when that file records none, use `[NO_TASK]`.
- During development on a single branch, intermediate commits are allowed. Before push, squash only the NEW commits added in this branch (not commits already present in `stayledger-cline`) into one with a task tag and a concise English summary describing the feature: `[<task-number>] <feature summary>` or `[NO_TASK] <feature summary>`. Use `git rebase -i` or `git reset --soft` onto `stayledger-cline` then commit once.
- Push only when explicitly requested or after `openspec archive <change-name>` has been completed for the current change.
- Before every push: `git fetch`, update `stayledger-cline` from `origin/stayledger-cline`, rebase the working branch onto `stayledger-cline`, then push.
- After a rebase push use `--force-with-lease`; never `--force`/`-f`.
- Never rewrite `stayledger-cline`; resolve conflicts only in the working branch.