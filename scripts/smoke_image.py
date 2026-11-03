#!/usr/bin/env python3
"""Run a versioned StayLedger image and verify its database-free health endpoint."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.request
import uuid
from pathlib import Path

from build_image import IMAGE_REPOSITORY, VERSION_PATTERN, assert_docker_available, default_version


ROOT = Path(__file__).resolve().parents[1]


def command(*args: str, capture: bool = False) -> str:
    result = subprocess.run(
        ["docker", *args], cwd=ROOT, check=False, capture_output=capture, text=True
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Docker command failed: {' '.join(args)}. {detail}")
    return result.stdout.strip() if capture else ""


def host_port(container: str) -> int:
    binding = json.loads(command("inspect", container, "--format", "{{json .NetworkSettings.Ports}}", capture=True))
    return int(binding["8081/tcp"][0]["HostPort"])


def wait_for_health(port: int, timeout: int) -> None:
    url = f"http://127.0.0.1:{port}/actuator/health"
    deadline = time.monotonic() + timeout
    last_error = "no response"
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                body = json.loads(response.read())
                if response.status == 200 and body.get("status") == "UP":
                    return
                last_error = f"HTTP {response.status}: {body}"
        except Exception as error:  # health polling must preserve the last useful diagnostic
            last_error = str(error)
        time.sleep(2)
    raise RuntimeError(f"Image did not become healthy at {url} within {timeout}s: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="Image version to smoke-test")
    parser.add_argument("--timeout", type=int, default=90, help="Health wait timeout in seconds")
    arguments = parser.parse_args()
    version = arguments.version or default_version()
    if not VERSION_PATTERN.fullmatch(version):
        raise RuntimeError(f"Unsupported image version: {version}")
    if arguments.timeout <= 0:
        raise RuntimeError("--timeout must be positive")

    assert_docker_available()
    container = f"stayledger-smoke-{uuid.uuid4().hex[:12]}"
    try:
        command("run", "--detach", "--rm", "--name", container, "--publish", "127.0.0.1::8081", f"{IMAGE_REPOSITORY}:{version}")
        wait_for_health(host_port(container), arguments.timeout)
    finally:
        subprocess.run(["docker", "rm", "--force", container], cwd=ROOT, check=False, capture_output=True)
    print(f"localhost:5000/stayledger:{version} is healthy without database variables")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
