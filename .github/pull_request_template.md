## OpenSpec archive warning

- [ ] No OpenSpec change is included, or every implemented change is archived under `openspec/changes/archive/` and its main capability spec is synced.

When creating this PR, run `python scripts/check_openspec_archive.py --base stayledger-codex --head HEAD`. If it reports an unarchived change, warn the author; this warning does not block PR creation.
