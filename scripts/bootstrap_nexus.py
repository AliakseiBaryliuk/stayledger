#!/usr/bin/env python3
"""Create the local Nexus Docker registry and its least-privilege publisher."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPOSITORY = "stayledger-hosted"
PUBLISHER_ROLE = "stayledger-docker-publisher"


def load_env_file(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Credential file does not exist: {path}")
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or not key:
            raise RuntimeError(f"Invalid environment line in {path}: {raw_line!r}")
        os.environ.setdefault(key, value)


def required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} must be set in the local environment file")
    return value


class NexusClient:
    def __init__(self, base_url: str, username: str, password: str) -> None:
        self.base_url = base_url.rstrip("/")
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.authorization = f"Basic {token}"

    def request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | str | None = None,
        allow_not_found: bool = False,
        allowed_statuses: set[int] | None = None,
    ) -> tuple[int, Any | None]:
        data = json.dumps(body).encode() if isinstance(body, dict) else body.encode() if body is not None else None
        headers = {"Authorization": self.authorization, "Accept": "application/json"}
        if data is not None:
            headers["Content-Type"] = "application/json" if isinstance(body, dict) else "text/plain"
        request = Request(f"{self.base_url}{path}", data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=15) as response:
                payload = response.read()
                return response.status, json.loads(payload) if payload else None
        except HTTPError as error:
            if allow_not_found and error.code == 404:
                return error.code, None
            if allowed_statuses and error.code in allowed_statuses:
                return error.code, None
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Nexus API {method} {path} failed with HTTP {error.code}: {detail}") from error
        except URLError as error:
            raise RuntimeError(f"Cannot reach Nexus at {self.base_url}: {error.reason}") from error


def wait_until_writable(client: NexusClient) -> None:
    deadline = time.monotonic() + 300
    while time.monotonic() < deadline:
        try:
            status, _ = client.request("GET", "/service/rest/v1/status/writable")
            if status == 200:
                return
        except RuntimeError:
            pass
        time.sleep(3)
    raise RuntimeError("Nexus did not become writable within five minutes")


def repository_payload() -> dict[str, Any]:
    return {
        "name": REPOSITORY,
        "online": True,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": True,
            "writePolicy": "ALLOW_ONCE",
            "latestPolicy": False,
        },
        "cleanup": {"policyNames": []},
        "docker": {"v1Enabled": False, "forceBasicAuth": False, "httpPort": 5000, "httpsPort": None},
    }


def ensure_repository(client: NexusClient) -> None:
    path = f"/service/rest/v1/repositories/docker/hosted/{REPOSITORY}"
    status, _ = client.request("GET", path, allow_not_found=True)
    if status == 404:
        client.request("POST", "/service/rest/v1/repositories/docker/hosted", repository_payload())
    else:
        client.request("PUT", path, repository_payload())


def ensure_publisher(client: NexusClient, username: str, password: str) -> None:
    privileges = [
        f"nx-repository-view-docker-{REPOSITORY}-browse",
        f"nx-repository-view-docker-{REPOSITORY}-read",
        f"nx-repository-view-docker-{REPOSITORY}-add",
        f"nx-repository-view-docker-{REPOSITORY}-edit",
    ]
    role_body = {
        "id": PUBLISHER_ROLE,
        "name": "StayLedger Docker publisher",
        "description": "Publishes immutable images to the local StayLedger registry.",
        "privileges": privileges,
        "roles": [],
    }
    role_path = f"/service/rest/v1/security/roles/{PUBLISHER_ROLE}"
    status, _ = client.request("GET", role_path, allow_not_found=True)
    if status == 404:
        client.request("POST", "/service/rest/v1/security/roles", role_body)
    else:
        client.request("PUT", role_path, role_body)

    user_body = {
        "userId": username,
        "firstName": "StayLedger",
        "lastName": "Publisher",
        "emailAddress": "stayledger-publisher@localhost",
        "status": "active",
        "source": "default",
        "roles": [PUBLISHER_ROLE],
    }
    create_user_body = {**user_body, "password": password}
    user_path = f"/service/rest/v1/security/users/{username}"
    # Nexus 3.96 returns DuplicateUserException as HTTP 500, while previous
    # releases report the same already-existing user as HTTP 400.
    status, _ = client.request(
        "POST", "/service/rest/v1/security/users", create_user_body, allowed_statuses={400, 500}
    )
    if status in {400, 500}:
        client.request("PUT", user_path, user_body)
        client.request("PUT", f"{user_path}/change-password", password)


def enable_anonymous_pull(client: NexusClient) -> None:
    client.request(
        "PUT",
        "/service/rest/v1/security/anonymous",
        {"enabled": True, "userId": "anonymous", "realmName": "NexusAuthorizingRealm"},
    )


def enable_docker_token_realm(client: NexusClient) -> None:
    _, realms = client.request("GET", "/service/rest/v1/security/realms/active")
    if not isinstance(realms, list):
        raise RuntimeError("Nexus returned an invalid active-realms response")
    if "DockerToken" not in realms:
        client.request("PUT", "/service/rest/v1/security/realms/active", realms + ["DockerToken"])


def accept_community_eula(client: NexusClient) -> None:
    _, status = client.request("GET", "/service/rest/v1/system/eula")
    if not isinstance(status, dict) or "accepted" not in status:
        raise RuntimeError("Nexus returned an invalid Community EULA response")
    if not status["accepted"]:
        disclaimer = status.get("disclaimer")
        if not isinstance(disclaimer, str) or not disclaimer:
            raise RuntimeError("Nexus returned an invalid Community EULA disclaimer")
        client.request("POST", "/service/rest/v1/system/eula", {"accepted": True, "disclaimer": disclaimer})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--env-file",
        type=Path,
        help="Optional ignored file containing Nexus credentials; environment variables also work.",
    )
    arguments = parser.parse_args()
    if arguments.env_file:
        load_env_file(arguments.env_file)

    client = NexusClient(
        os.environ.get("NEXUS_URL", "http://127.0.0.1:8082"),
        os.environ.get("NEXUS_ADMIN_USERNAME", "admin"),
        required("NEXUS_ADMIN_PASSWORD"),
    )
    wait_until_writable(client)
    accept_community_eula(client)
    ensure_repository(client)
    ensure_publisher(client, required("NEXUS_PUBLISHER_USERNAME"), required("NEXUS_PUBLISHER_PASSWORD"))
    enable_docker_token_realm(client)
    enable_anonymous_pull(client)
    print(f"Nexus Docker repository '{REPOSITORY}' is ready at localhost:5000.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
