# Stage 2 — Versioning and Docker Image

**Proposed branch:** `chore/delivery-versioning`
**Dependencies:** stage 1

## Objective

Determine the Gradle artifact, application metadata, Docker image, and future Helm release versions consistently, without manually changing versions before each build.

## Versioning Approach

- The source of the release version is the latest annotated Git tag in `vX.Y.Z` format; the initial baseline is `v0.1.0`, matching the current project version.
- The next version increments the patch of the latest release tag: after `v0.1.0`, it is `0.1.1`.
- `feature/*`, `fix/*`, and `chore/*` branches receive `0.1.1-SNAPSHOT`; the Docker tag also contains an immutable short commit SHA or build number.
- On `stayledger-codex`, a successful release build receives `0.1.1`, publishes its corresponding immutable image, and only then creates `v0.1.1`. Recreating a tag fails the process.
- For a minor or major release, a new annotated baseline tag is created before merge through the agreed release process; the automated path increments only the patch.

## Changes

- Add a script or Gradle logic that passes the calculated version through `-PappVersion`; do not duplicate it in Docker or Helm configuration.
- Create a production-oriented multi-stage Dockerfile and `.dockerignore`; the final image runs as an unprivileged user and excludes Git data, IDE files, and secrets.
- Pass the version explicitly to the JAR and Docker build; base the startup command on the actual boot JAR.

## Out of Scope

- Registry publishing, Kubernetes deployment, and Jenkins orchestration.

## Acceptance Criteria

- The Gradle JAR and Docker image have one calculated version.
- The image builds and starts locally without embedded secrets.
- Version checks cover release, snapshot, and an attempt to reuse a release tag.
