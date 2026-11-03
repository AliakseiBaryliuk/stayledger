# delivery-versioning Specification

## Purpose

Provide a reproducible local container delivery path that turns the configured
StayLedger application version into a secure OCI image and distributes it
through a local immutable registry.

## Requirements

### Requirement: Calculated application image version
The delivery tooling SHALL build the `_ms` boot JAR and OCI image with one
calculated version, using the branch default unless `appVersion` is explicitly
provided. The local image reference SHALL be
`localhost:5000/stayledger:<version>`.

#### Scenario: Default version build
- **WHEN** an operator builds the image without an application version override
- **THEN** the boot JAR and image tag use the version configured for the branch

#### Scenario: Explicit release version build
- **WHEN** an operator builds the image with `appVersion=0.2.3-RELEASE`
- **THEN** the boot JAR and image tag both use `0.2.3-RELEASE`

### Requirement: Secure runnable application image
The published OCI image SHALL contain only the runtime application artifacts,
run as an unprivileged user, listen on port 8081, and contain no source-control
metadata or credentials.

#### Scenario: Image starts without database configuration
- **WHEN** an operator starts the built image without PostgreSQL credentials
- **THEN** the image starts and serves the technical health endpoint on port 8081

#### Scenario: Runtime image inspection
- **WHEN** an operator inspects the built runtime image
- **THEN** its configured user is not root and its filesystem does not include build context secrets or Git metadata

### Requirement: Local immutable image registry
The local delivery environment SHALL provide a Nexus Docker hosted repository
at `127.0.0.1:5000` with authenticated image push, anonymous image pull, and
immutable image tags.

#### Scenario: Authenticated image publication
- **WHEN** an authenticated publisher pushes `localhost:5000/stayledger:0.2.3`
- **THEN** the registry accepts the image and an unauthenticated local client can pull it

#### Scenario: Duplicate tag publication
- **WHEN** a publisher attempts to push a different image using an existing tag
- **THEN** the registry rejects the publication
