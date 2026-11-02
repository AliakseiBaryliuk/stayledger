#!/usr/bin/env python3
"""Reject a pull request that carries an unarchived OpenSpec change."""

import argparse
import re
import subprocess
import sys


ARCHIVE_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")
TAG = re.compile(r"^\[([^]]+)\]")
CHANGE_NAME = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def git(*args: str) -> str:
    return subprocess.check_output(("git", *args), text=True).strip()


def change_from_path(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) < 4 or parts[:2] != ["openspec", "changes"]:
        return None
    if parts[2] == "archive":
        if len(parts) < 5:
            return None
        match = ARCHIVE_NAME.fullmatch(parts[3])
        return match.group(1) if match else None
    return parts[2]


def unarchived_changes(base: str, head: str) -> list[str]:
    changed = git("diff", "--name-only", "--no-renames", f"{base}...{head}").splitlines()
    head_paths = git("ls-tree", "-r", "--name-only", head, "--", "openspec/changes").splitlines()
    active = set()
    archived = set()
    for path in head_paths:
        parts = path.split("/")
        if len(parts) < 4 or parts[:2] != ["openspec", "changes"]:
            continue
        if parts[2] == "archive":
            if len(parts) >= 5:
                match = ARCHIVE_NAME.fullmatch(parts[3])
                if match:
                    archived.add(match.group(1))
        else:
            active.add(parts[2])

    relevant = {name for path in changed if (name := change_from_path(path))}
    for subject in git("log", "--format=%s", f"{base}..{head}").splitlines():
        match = TAG.match(subject)
        if match:
            tag = match.group(1)
            if tag in active or tag in archived or CHANGE_NAME.fullmatch(tag):
                relevant.add(tag)

    return sorted(name for name in relevant if name in active or name not in archived)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="PR base commit SHA")
    parser.add_argument("--head", required=True, help="PR head commit SHA")
    args = parser.parse_args()

    try:
        missing = unarchived_changes(args.base, args.head)
    except subprocess.CalledProcessError as error:
        print(f"Could not inspect PR commits: {error}", file=sys.stderr)
        return 2

    if missing:
        print("OpenSpec archive is required before this PR can merge:", file=sys.stderr)
        for name in missing:
            print(f"  - {name}: run the archive workflow and commit openspec/changes/archive/YYYY-MM-DD-{name}/", file=sys.stderr)
        return 1

    print("OpenSpec archive check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
