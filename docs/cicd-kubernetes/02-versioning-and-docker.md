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

## Out of Scope

- Registry publishing, Kubernetes deployment, Jenkins orchestration, and merge-queue implementation.

## Acceptance Criteria

- The Gradle JAR and Docker image have one calculated version, whether it comes from `gradle.properties` or `-PappVersion`.
- The image builds and starts locally without embedded secrets.
- Version checks cover normal release, release-fix, SNAPSHOT, production `-RELEASE`, marker tags, and an attempt to reuse a tag.
