#!/usr/bin/env python3
"""Build and optionally push the StayLedger image with one explicit version."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-(?:SNAPSHOT|RELEASE))?$")
IMAGE_REPOSITORY = "localhost:5000/stayledger"
ROOT = Path(__file__).resolve().parents[1]


def default_version() -> str:
    for line in (ROOT / "gradle.properties").read_text(encoding="utf-8").splitlines():
        if line.startswith("version="):
            return line.removeprefix("version=").strip()
    raise RuntimeError("gradle.properties does not define version")


def run(command: list[str]) -> None:
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except FileNotFoundError as error:
        raise RuntimeError("Docker CLI is not installed or is not on PATH") from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"Command failed with exit code {error.returncode}: {' '.join(command)}") from error


def assert_docker_available() -> None:
    try:
        result = subprocess.run(
            ["docker", "info"], cwd=ROOT, capture_output=True, text=True, check=False
        )
    except FileNotFoundError as error:
        raise RuntimeError("Docker CLI is not installed or is not on PATH") from error
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Docker daemon is unavailable. Start Docker Desktop and retry. {detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="Version to pass to Gradle and use as the image tag")
    parser.add_argument("--push", action="store_true", help="Push the built image after a successful build")
    arguments = parser.parse_args()

    version = arguments.version or default_version()
    if not VERSION_PATTERN.fullmatch(version):
        raise RuntimeError(f"Unsupported image version: {version}")
    image = f"{IMAGE_REPOSITORY}:{version}"

    assert_docker_available()
    run(["docker", "build", "--build-arg", f"APP_VERSION={version}", "--tag", image, "."])
    if arguments.push:
        run(["docker", "push", image])
    print(image)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
