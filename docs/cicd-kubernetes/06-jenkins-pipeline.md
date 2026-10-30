# Stage 6 — Jenkins Pipeline

**Proposed branch:** `feature/jenkins-pipeline`  
**Dependencies:** stages 1–5

## Objective

Automate validation, build, and release/deploy workflows using the already verified local commands.

## Pipeline Contract

- The Jenkins agent runs on a host with Java 21, Docker CLI and daemon, Gradle Wrapper, kubectl, Helm, and access to the required Minikube profile. A privileged Jenkins container and Docker socket are not the supported default topology.
- `feature/*`, `fix/*`, and `chore/*` branches run validation and create a SNAPSHOT artifact, but do not perform a release deployment.
- `stayledger-codex` runs the release path: version calculation, tests, JAR, image, image delivery to Minikube, Helm validation, upgrade, rollout, and an HTTP smoke test.
- The pipeline serializes the release path so that two merges cannot calculate the same next patch. The Git tag is pushed only after a successful rollout.
- The Git-tag token, registry credentials if introduced, and Kubernetes secrets are used only from Jenkins Credentials Store and are never printed in logs.

## Changes

- Add a `Jenkinsfile` with timeouts, fail-fast behavior, and temporary-resource cleanup.
- Invoke the same Gradle, Docker, and Helm scripts as the local runbook; do not duplicate versioning logic in Groovy.
- Document Jenkins credential setup and host-based topology limitations.

## Acceptance Criteria

- A test, build, image build, Helm validation, rollout, or smoke-test failure prevents deployment and tagging.
- The release branch creates exactly one new semver tag, and a working branch does not publish a release.
- Pipeline logs contain no credential values.
