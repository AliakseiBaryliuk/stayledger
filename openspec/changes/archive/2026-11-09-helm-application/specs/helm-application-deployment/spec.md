# Spec Delta

## Purpose

Provide a reproducible Helm release for operating the StayLedger application
on Kubernetes without storing runtime credentials in the source repository.

## ADDED Requirements

### Requirement: Installable application Helm release
The system SHALL provide a Helm chart that renders the application Deployment,
ClusterIP Service, and ConfigMap into the namespace selected for the release.

#### Scenario: Render a local release
- **WHEN** an operator runs `helm template` with the chart's local values
- **THEN** the rendered manifest contains one Deployment, one ClusterIP Service,
  and one ConfigMap in the selected release namespace

### Requirement: Configurable immutable application image
The Helm release SHALL allow operators to configure the application image
repository and tag independently through chart values.

#### Scenario: Override image coordinates
- **WHEN** an operator supplies image repository and tag values during rendering
- **THEN** the Deployment container image uses the supplied repository and tag

### Requirement: External sensitive configuration
The Helm chart SHALL reference an operator-managed Kubernetes Secret for the
`DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` container environment variables and
SHALL NOT render Secret data or password values.

#### Scenario: Render with an existing Secret reference
- **WHEN** an operator supplies the name and key mapping of an existing Secret
- **THEN** the Deployment references that Secret for all three database
  environment variables and no Secret resource or credential value is rendered

### Requirement: Non-sensitive runtime configuration
The Helm chart SHALL render non-sensitive runtime configuration in a ConfigMap
and make it available to the application container without exposing database
credentials.

#### Scenario: Override a non-sensitive runtime value
- **WHEN** an operator changes a supported non-sensitive configuration value
- **THEN** the ConfigMap and application container reflect that value while the
  database credentials remain Secret references

### Requirement: Health-aware rolling updates
The Helm release SHALL configure resource requests and limits, a rolling update
strategy, and HTTP liveness and readiness probes on application port 8081.

#### Scenario: Render health checks
- **WHEN** an operator renders the chart with local values
- **THEN** the Deployment probes `/actuator/health/liveness` and
  `/actuator/health/readiness` on port 8081 and retains configured rollout and
  resource settings

### Requirement: Stable in-cluster application endpoint
The Helm release SHALL expose the application through a ClusterIP Service that
selects the release Deployment and forwards port 8081 to the container.

#### Scenario: Render the application Service
- **WHEN** an operator renders the chart
- **THEN** the Service is ClusterIP, selects the Deployment labels, and maps its
  application port to container port 8081
