# Stage 2 — Versioning and Docker Image

**Proposed branch:** `chore/delivery-versioning`
**Dependencies:** stage 1

## Objective

Determine the Gradle artifact, application metadata, Docker image, and future Helm release versions consistently across develop, release, and production lines.

## Versioning Approach

- `gradle.properties` stores the default version of its branch. `-PappVersion` overrides it for a calculated build version without changing the file.
- The baseline is annotated `v0.1.0` on `stayledger-codex`. Bootstrap sets develop to `version=0.2.0-SNAPSHOT` and creates the `v0.2.0` marker; markers publish nothing.
- A normal working branch from develop builds the next patch SNAPSHOT. For example, from develop `0.2.2`, it builds `0.2.3-SNAPSHOT`. Its serialized merge creates a technical `version=0.2.3` commit, annotated `v0.2.3`, and immutable JAR/Docker artifacts without production deployment.
- A release is cut as `release/RL-xx` from a stable develop version. The cut advances develop to the next minor through a technical `version=X.(Y+1).0-SNAPSHOT` commit and marker tag, without publication.
- Release fixes use `fix/RL-xx/<short-topic>`, build the next patch SNAPSHOT of that release line, and merge through that release branch's queue. The queue creates the technical patch commit, `vX.Y.Z`, and immutable non-production artifacts.
- Each release merge opens a sync PR back to develop. It retains develop's `gradle.properties`; any functional conflict blocks final promotion.
- The final PR is only `release/RL-xx` -> `stayledger-codex`. It rebuilds with `-PappVersion=X.Y.Z-RELEASE`, deploys that exact production image, then creates `vX.Y.Z-RELEASE`. Recreating any annotated tag fails.

## Changes

- Add Gradle logic that reads the default version from `gradle.properties` and accepts a calculated override through `-PappVersion`; do not duplicate it in Docker or Helm configuration.
- Create a production-oriented multi-stage Dockerfile and `.dockerignore`; the final image runs as an unprivileged user and excludes Git data, IDE files, and secrets.
- Pass the version explicitly to the JAR and Docker build; base the startup command on the actual boot JAR.
- Run a local, loopback-only Nexus Docker hosted repository for repeatable non-production image publication. The local endpoint is `localhost:5000`; it is not a remote or production registry.

## Out of Scope

- Kubernetes deployment, Jenkins orchestration, merge-queue implementation, and remote-registry publication.

## Local Nexus registry

Docker Desktop must be running. The registry is deliberately limited to the
local machine: its UI/API is `127.0.0.1:8082` and its Docker endpoint is
`127.0.0.1:5000`. Nexus persists its state in the Compose volume
`nexus-data`.

1. Copy `docker/nexus/.env.example` to `docker/nexus/.env`, choose a strong
   publisher password, and leave the administrator password empty initially.
   The local `.env` file is ignored by Git.
2. Start Nexus:

   ```powershell
   docker compose --env-file docker/nexus/.env -f docker/nexus/compose.yaml up -d
   ```

3. Once Nexus has started, obtain its generated initial password without
   printing any configured publisher credential:

   ```powershell
   docker compose --env-file docker/nexus/.env -f docker/nexus/compose.yaml exec nexus cat /nexus-data/admin.password
   ```

   Put that value in `NEXUS_ADMIN_PASSWORD` in `docker/nexus/.env`, then run
   the idempotent bootstrap:

   ```powershell
   python scripts/bootstrap_nexus.py --env-file docker/nexus/.env
   ```

   It records acceptance of the Nexus Community EULA for this local instance,
   creates `stayledger-hosted` with the immutable `ALLOW_ONCE` policy,
   configures the publisher role, and enables anonymous read access. Docker
   engines that do not trust a loopback HTTP registry must be configured to
   allow `localhost:5000` as an insecure registry.

4. Authenticate only when publishing. The command reads the ignored local
   credential file and passes the password through standard input; do not put
   its input or generated Docker credentials in source control:

   ```powershell
   python scripts/nexus_login.py --env-file docker/nexus/.env
   ```

## Image commands

The reusable commands use `gradle.properties` by default. `--version` is the
single version passed both to Gradle (`-PappVersion`) and to the Docker image
tag. They fail immediately with a prerequisite message when Docker is not
running.

```powershell
# Default branch version, currently 0.2.0-SNAPSHOT.
python scripts/build_image.py

# Calculated topic/release build, then smoke-test it without database variables.
python scripts/build_image.py --version 0.2.3-SNAPSHOT
python scripts/smoke_image.py --version 0.2.3-SNAPSHOT

# Publish an immutable non-production or final-release tag after the smoke test.
python scripts/build_image.py --version 0.2.3 --push
python scripts/build_image.py --version 0.2.3-RELEASE --push
```

Each command publishes or tests `localhost:5000/stayledger:<version>`. A
second push of the same tag is rejected by Nexus. A local consumer can pull a
published image anonymously:

```powershell
docker image rm localhost:5000/stayledger:0.2.3
docker pull localhost:5000/stayledger:0.2.3
```

## Acceptance Criteria

- The Gradle JAR and Docker image have one calculated version, whether it comes from `gradle.properties` or `-PappVersion`.
- The image builds and starts locally without embedded secrets; its runtime user is non-root and it exposes the existing health endpoint on port 8081 without database variables.
- A publisher can push to the local Nexus repository, an anonymous consumer can pull, and a duplicate immutable tag is rejected.
- Version checks cover normal release, release-fix, SNAPSHOT, production `-RELEASE`, marker tags, and an attempt to reuse a tag.
