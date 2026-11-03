#!/usr/bin/env python3
"""Authenticate Docker to the local Nexus registry without exposing a password."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from bootstrap_nexus import load_env_file, required


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--env-file",
        type=Path,
        help="Optional ignored file containing Nexus publisher credentials.",
    )
    arguments = parser.parse_args()
    if arguments.env_file:
        load_env_file(arguments.env_file)

    try:
        result = subprocess.run(
            ["docker", "login", "localhost:5000", "--username", required("NEXUS_PUBLISHER_USERNAME"), "--password-stdin"],
            input=required("NEXUS_PUBLISHER_PASSWORD"),
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        raise RuntimeError("Docker CLI is not installed or is not on PATH") from error
    if result.returncode != 0:
        raise RuntimeError("Docker login to localhost:5000 failed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
