# Proposal

## Why

StayLedger has a branch-owned Gradle version but cannot yet produce a secure,
versioned container image or distribute it through a local registry. A
repeatable local delivery path is needed before Helm and Jenkins automation can
use the same artifact lifecycle.

## What Changes

- Add a production-oriented, multi-stage Docker image build for the `_ms`
  Spring Boot application.
- Use the Gradle-calculated version for the boot JAR, image tag, and optional
  `-PappVersion` override.
- Add a local, loopback-only Nexus Repository Compose deployment with an
  immutable Docker hosted repository, authenticated push, and anonymous pull.
- Add shared local build, registry bootstrap, push, and smoke-test commands
  without implementing Jenkins or merge-queue automation.
- Update the Stage 2 delivery documentation for the Nexus-backed image flow.

## Capabilities

### New Capabilities

- `delivery-versioning`: Builds, tags, verifies, and locally distributes
  versioned StayLedger OCI images.

### Modified Capabilities

- None.

## Impact

- Affects Gradle build configuration, Docker/Compose assets, local developer
  prerequisites, and Stage 2 documentation.
- Introduces Nexus Repository as a local external service at loopback-only
  endpoints and Docker image references under `localhost:5000`.
- Does not change application HTTP behavior, database behavior, Kubernetes
  deployment, registry publication outside the local machine, or Jenkins.
