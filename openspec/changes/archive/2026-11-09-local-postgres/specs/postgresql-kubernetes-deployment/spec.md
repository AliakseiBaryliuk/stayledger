# Spec Delta

## Purpose

Provide a reproducible local PostgreSQL service on Kubernetes that persists its
data and securely supplies the StayLedger application connection settings.

## ADDED Requirements

### Requirement: Pinned local PostgreSQL release
The system SHALL provide an operator-installable PostgreSQL Helm release in the
application namespace using a documented, version-pinned chart and a standalone
database Service reachable within that namespace.

#### Scenario: Install the local database release
- **WHEN** an operator installs the documented PostgreSQL release with its local values
- **THEN** Kubernetes creates a ready PostgreSQL workload and an in-namespace Service endpoint for the database

### Requirement: Persistent database storage
The PostgreSQL release SHALL request persistent storage through a ReadWriteOnce
PersistentVolumeClaim when the selected Minikube driver provides a compatible
StorageClass, and it SHALL retain the claim when the database workload is
removed.

#### Scenario: Provision storage with a compatible driver
- **WHEN** the local cluster has a compatible default StorageClass and the operator installs PostgreSQL
- **THEN** the database workload binds a PersistentVolumeClaim and retains database data across a workload recreation

#### Scenario: Intentionally remove database data
- **WHEN** an operator follows the documented destructive cleanup procedure
- **THEN** the procedure identifies the exact PersistentVolumeClaim to delete and warns that its data cannot be recovered

### Requirement: External database credentials and connection settings
The PostgreSQL release and StayLedger application release SHALL consume database
credentials from an operator-managed Kubernetes Secret; neither Helm release
nor repository files SHALL render or contain credential values. The application
connection URL SHALL use the PostgreSQL Service DNS name rather than `localhost`.

#### Scenario: Create and consume the local runtime Secret
- **WHEN** an operator creates the documented Secret in the application namespace and installs both releases
- **THEN** PostgreSQL receives its configured credential keys and the application Deployment references `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` from that Secret

#### Scenario: Render deployment assets
- **WHEN** an operator renders the PostgreSQL and StayLedger Helm releases with local values
- **THEN** the rendered manifests contain Secret references but no credential values and the application `DB_URL` targets the PostgreSQL Service DNS name

### Requirement: Operable local database lifecycle
The local deployment documentation SHALL define readiness verification,
connection diagnostics, a chart upgrade procedure, and the credential/PVC
constraints that apply to existing database data.

#### Scenario: Verify a deployed local stack
- **WHEN** an operator completes the documented readiness and rollout checks
- **THEN** the checks confirm database readiness and a successful StayLedger application rollout with the configured Secret references
