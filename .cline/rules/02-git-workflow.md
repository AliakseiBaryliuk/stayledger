# Git workflow

Follow `docs/git-workflow.md`. The integration branch is `master`.

- When starting a new OpenSpec flow, create a new branch from `master` and work on it.
- Never commit or push directly to `master`; land changes via a branch plus a pull request.
- Commit subjects start with a task tag plus a concise English summary: `[NO_TASK] <summary>` when there is no tracker task, `[<task-number>] <summary>` when there is one. Never invent a number.
- The `[<task-number>]` tag must match the task id recorded in the `package-info.java` of the mini-scenario the change touches; when that file records none, use `[NO_TASK]`.
- During development on a single branch, intermediate commits are allowed. Before push, squash only the NEW commits added in this branch (not commits already present in master) into one with a task tag and a concise English summary describing the feature: `[<task-number>] <feature summary>` or `[NO_TASK] <feature summary>`. Use `git rebase -i` or `git reset --soft` onto `master` then commit once.
- Push only when explicitly requested or after `openspec archive <change-name>` has been completed for the current change.
- Before every push: `git fetch`, update `master` from `origin/master`, rebase the working branch onto `master`, then push.
- After a rebase push use `--force-with-lease`; never `--force`/`-f`.
- Never rewrite `master`; resolve conflicts only in the working branch.