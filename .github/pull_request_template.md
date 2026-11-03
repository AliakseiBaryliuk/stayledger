## OpenSpec archive warning

- [ ] No OpenSpec change is included, or every implemented change is archived under `openspec/changes/archive/` and its main capability spec is synced.

Before creating this PR, use its target branch as `--base`:

- Normal PR: `python scripts/check_openspec_archive.py --base stayledger-codex-develop --head HEAD`
- Release fix: `python scripts/check_openspec_archive.py --base release/RL-xx --head HEAD`
- Final release: `python scripts/check_openspec_archive.py --base stayledger-codex --head HEAD`

If it reports an unarchived change, warn the author; this warning does not block PR creation.
