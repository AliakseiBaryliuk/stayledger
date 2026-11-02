# Spec Delta

## Purpose

Provide technical HTTP checks and runtime measurements so local operators, Kubernetes, and Prometheus can observe the application independently of business capabilities.

## ADDED Requirements

### Requirement: Default HTTP port
The application SHALL listen on port 8081 by default unless its server port is explicitly overridden.

#### Scenario: Application starts with default configuration
- **WHEN** the application starts without a server port override
- **THEN** its HTTP server listens on port 8081

### Requirement: Technical HTTP availability
The application SHALL respond to GET `/internal/ping` with HTTP 200 without executing business behavior.

#### Scenario: Running application responds to a technical request
- **WHEN** a client sends GET `/internal/ping` to the application port
- **THEN** the application responds with HTTP 200

### Requirement: Runtime health probes
The application SHALL expose overall health, liveness, and readiness at `/actuator/health`, `/actuator/health/liveness`, and `/actuator/health/readiness` respectively.

#### Scenario: Healthy application reports overall health
- **WHEN** a client requests `/actuator/health` while the application is healthy
- **THEN** the response has HTTP 200 and reports `UP`

#### Scenario: Live application reports liveness
- **WHEN** a client requests `/actuator/health/liveness` after startup
- **THEN** the response has HTTP 200 and reports `UP`

#### Scenario: Ready application reports readiness
- **WHEN** a client requests `/actuator/health/readiness` after startup completes
- **THEN** the response has HTTP 200 and reports `UP`

### Requirement: Prometheus runtime metrics
The application SHALL expose runtime metric samples at `/actuator/prometheus` in Prometheus exposition format.

#### Scenario: Metrics scrape
- **WHEN** a client requests `/actuator/prometheus` from the running application
- **THEN** the response has HTTP 200 and contains Prometheus-compatible metric samples

### Requirement: Limited management exposure
The application SHALL expose only the `health` and `prometheus` Actuator endpoints over HTTP in this stage.

#### Scenario: Another Actuator endpoint is requested
- **WHEN** a client requests another Actuator endpoint over HTTP
- **THEN** that endpoint is not exposed

### Requirement: Startup without database access
The application SHALL start and serve technical endpoints without PostgreSQL credentials or a PostgreSQL connection in this stage.

#### Scenario: No database is configured
- **WHEN** the application starts without database environment variables or a running PostgreSQL server
- **THEN** it serves `/internal/ping` and the runtime health probes
