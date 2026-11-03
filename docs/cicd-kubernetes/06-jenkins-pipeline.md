# Stage 6 — Jenkins Pipeline

**Proposed branch:** `feature/jenkins-pipeline`
**Dependencies:** stages 1–5

## Objective

Automate validation, build, and release/deploy workflows using the already verified local commands.

## Pipeline Contract

- The Jenkins agent runs on a host with Java 21, Docker CLI and daemon, Gradle Wrapper, kubectl, Helm, and access to the required Minikube profile. A privileged Jenkins container and Docker socket are not the supported default topology.
- `feature/*`, `fix/*`, and `chore/*` branches target `stayledger-codex-develop`; they run validation and build the next patch SNAPSHOT without publishing a release or deploying.
- Merge queues serialize PRs into `stayledger-codex-develop` and each `release/RL-xx` branch. They recalculate the next patch, create the technical version commit, then build and publish the annotated non-production `vX.Y.Z` artifact.
- A release cut creates `release/RL-xx` from develop and advances develop to the next minor through a marker tag without publication. Release fixes target their release branch and automatically create a sync PR back to develop after merging.
- A functional conflict in the sync PR blocks the final release. Only `release/RL-xx` may target `stayledger-codex`.
- `stayledger-codex` runs the production path after the final release PR: tests, JAR/image build with `-PappVersion=X.Y.Z-RELEASE`, image delivery to Minikube, Helm validation, upgrade, rollout, and an HTTP smoke test. It then creates `vX.Y.Z-RELEASE`.
- Queues and the production path serialize tag creation so no tag can be reused. The production tag is pushed only after a successful rollout.
- The Git-tag token, registry credentials if introduced, and Kubernetes secrets are used only from Jenkins Credentials Store and are never printed in logs.

## Changes

- Add a `Jenkinsfile` with timeouts, fail-fast behavior, and temporary-resource cleanup.
- Invoke the same Gradle, Docker, and Helm scripts as the local runbook; do not duplicate versioning logic in Groovy.
- Document Jenkins credential setup and host-based topology limitations.

## Acceptance Criteria

- A test, build, image build, Helm validation, rollout, or smoke-test failure prevents production deployment and its `-RELEASE` tag.
- A working branch does not publish a release. Develop and release queues create only the next patch tag for their target line; release-cut markers publish no artifact.
- A final release cannot merge while a release-to-develop sync PR is blocked or unmerged.
- Pipeline logs contain no credential values.
