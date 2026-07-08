# Backend Low-Level Design

## Project Name

Industrial Edge Monitoring Platform

## 1. Purpose

This document defines the low-level backend design for the Industrial Edge Monitoring Platform.

It explains the backend folder structure, layer responsibilities, coding rules, dependency flow, error handling approach, configuration strategy, and design patterns used in the backend service.

The goal is to keep the backend production-grade, testable, maintainable, and scalable.

---

## 2. Backend Technology Stack

The backend will use:

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic
* PostgreSQL
* TimescaleDB
* Pytest
* Ruff
* Mypy
* Docker
* OpenTelemetry
* Prometheus client

---

## 3. Backend Architecture Style

The backend will follow a layered architecture inspired by Clean Architecture.

```text
API Layer
    ↓
Schema Layer
    ↓
Service Layer
    ↓
Repository Layer
    ↓
Database Model Layer
```

The dependency direction should always go inward/downward.

Allowed flow:

```text
API → Service → Repository → Database Model
```

Not allowed:

```text
Repository → API
Service → API
Database Model → Service
API → Database directly
```

---

## 4. Backend Folder Structure

The backend folder will be structured as follows:

```text
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routers/
│   │   │   │   ├── health.py
│   │   │   │   ├── devices.py
│   │   │   │   ├── telemetry.py
│   │   │   │   ├── alerts.py
│   │   │   │   └── auth.py
│   │   │   └── api_router.py
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   └── constants.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   │
│   ├── models/
│   │   ├── device.py
│   │   ├── telemetry.py
│   │   ├── quarantine.py
│   │   ├── alert.py
│   │   ├── user.py
│   │   └── audit_log.py
│   │
│   ├── schemas/
│   │   ├── device.py
│   │   ├── telemetry.py
│   │   ├── quarantine.py
│   │   ├── alert.py
│   │   ├── auth.py
│   │   └── common.py
│   │
│   ├── repositories/
│   │   ├── device_repository.py
│   │   ├── telemetry_repository.py
│   │   ├── quarantine_repository.py
│   │   ├── alert_repository.py
│   │   └── audit_log_repository.py
│   │
│   ├── services/
│   │   ├── device_service.py
│   │   ├── telemetry_service.py
│   │   ├── alert_service.py
│   │   ├── auth_service.py
│   │   └── audit_service.py
│   │
│   ├── security/
│   │   ├── jwt.py
│   │   ├── api_key.py
│   │   ├── password.py
│   │   └── permissions.py
│   │
│   ├── workers/
│   │   ├── alert_worker.py
│   │   └── telemetry_worker.py
│   │
│   ├── observability/
│   │   ├── metrics.py
│   │   ├── tracing.py
│   │   └── log_context.py
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   └── conftest.py
│
├── alembic/
├── pyproject.toml
├── Dockerfile
└── README.md
```

---

## 5. Layer Responsibilities

## 5.1 API Layer

Location:

```text
app/api/
```

Responsibilities:

* define FastAPI routes
* accept HTTP requests
* return HTTP responses
* call service layer
* define status codes
* use dependency injection
* handle request-level dependencies

Rules:

* API layer must not directly call SQLAlchemy models.
* API layer must not contain business rules.
* API layer must not know database implementation details.
* API layer can call services only.

Example:

```python
@router.post("/devices")
def create_device(payload: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    return service.create_device(payload)
```

---

## 5.2 Schema Layer

Location:

```text
app/schemas/
```

Responsibilities:

* define request models
* define response models
* validate API payloads
* define reusable common schemas

Technology:

* Pydantic

Rules:

* Schemas represent API contracts.
* Schemas should not contain database logic.
* Schemas should not expose internal database-only fields unless required.
* Separate create, update, and response schemas should be used.

Example schema types:

```text
DeviceCreate
DeviceUpdate
DeviceResponse
DeviceListResponse
```

---

## 5.3 Service Layer

Location:

```text
app/services/
```

Responsibilities:

* implement business rules
* orchestrate workflows
* validate business constraints
* call repositories
* call audit service when needed
* decide which exception should be raised

Rules:

* Services must not know HTTP status codes directly.
* Services should raise domain/application exceptions.
* Services should not directly expose SQLAlchemy models to API layer.
* Services should coordinate one or more repositories.

Example responsibilities:

```text
DeviceService.create_device()
DeviceService.disable_device()
TelemetryService.ingest_telemetry()
AlertService.acknowledge_alert()
```

---

## 5.4 Repository Layer

Location:

```text
app/repositories/
```

Responsibilities:

* database queries
* inserts
* updates
* deletes where allowed
* fetching records by ID
* checking existence
* applying pagination filters

Rules:

* Repositories should not contain business rules.
* Repositories should not know HTTP status codes.
* Repositories should not validate API payloads.
* Repositories should return database entities or persistence results.

Example responsibilities:

```text
DeviceRepository.get_by_device_id()
DeviceRepository.create()
DeviceRepository.exists_by_device_id()
TelemetryRepository.create()
AlertRepository.find_open_alert()
```

---

## 5.5 Database Model Layer

Location:

```text
app/models/
```

Responsibilities:

* define SQLAlchemy ORM models
* define table names
* define columns
* define indexes
* define relationships
* define database constraints

Rules:

* Models should represent persistence structure.
* Models should not contain API validation logic.
* Models should not contain business workflows.

---

## 6. Dependency Injection Design

FastAPI dependency injection will be used to provide:

* database sessions
* repositories
* services
* current user
* current device
* authorization checks

Location:

```text
app/api/dependencies.py
```

Example dependency flow:

```text
get_db_session()
    ↓
get_device_repository()
    ↓
get_device_service()
    ↓
API route
```

This improves testability because dependencies can be replaced in tests.

---

## 7. Error Handling Design

The backend will use controlled application exceptions.

Location:

```text
app/core/exceptions.py
```

Common exception types:

```text
ApplicationError
ValidationError
NotFoundError
ConflictError
UnauthorizedError
ForbiddenError
ExternalServiceError
```

Exception mapping:

| Exception            | HTTP Status |
| -------------------- | ----------- |
| ValidationError      | 422         |
| NotFoundError        | 404         |
| ConflictError        | 409         |
| UnauthorizedError    | 401         |
| ForbiddenError       | 403         |
| ExternalServiceError | 502         |
| Unexpected Error     | 500         |

Rules:

* Services raise application exceptions.
* API/global exception handlers convert exceptions to HTTP responses.
* Internal error details should not be exposed to clients.
* All unexpected errors should be logged with correlation_id.

---

## 8. Configuration Design

Application configuration will be environment-based.

Location:

```text
app/core/config.py
```

Configuration values:

```text
APP_NAME
APP_ENV
LOG_LEVEL
DATABASE_URL
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
DEVICE_API_KEY_HEADER
ENABLE_METRICS
ENABLE_TRACING
```

Rules:

* No secrets in code.
* No production secrets in default values.
* Use environment variables.
* Local development may use `.env`.
* `.env` must not be committed.
* `.env.example` may be committed.

---

## 9. Logging Design

The backend will use structured logging.

Location:

```text
app/core/logging.py
```

Each log should include:

```text
timestamp
level
service_name
environment
correlation_id
message
module
```

Request logs should include:

```text
method
path
status_code
duration_ms
client_ip
```

Sensitive values must be masked:

```text
Authorization
X-Device-Api-Key
password
token
secret
```

---

## 10. Middleware Design

Middleware will be used for cross-cutting concerns.

Location:

```text
app/core/middleware.py
```

Planned middleware:

```text
CorrelationIdMiddleware
RequestLoggingMiddleware
SecurityHeadersMiddleware
```

Responsibilities:

* generate or reuse correlation ID
* attach correlation ID to response headers
* log request start and completion
* add basic security headers

---

## 11. Observability Design

The backend will expose:

```text
/health
/live
/ready
/metrics
```

Observability components:

```text
structured logs
Prometheus metrics
OpenTelemetry traces
correlation ID
```

Metrics examples:

```text
http_requests_total
http_request_duration_seconds
telemetry_events_received_total
telemetry_events_invalid_total
alerts_created_total
database_errors_total
```

---

## 12. Database Transaction Design

For the initial version, repository methods will use a database session passed through dependency injection.

Later, if workflows become complex, we can introduce a Unit of Work pattern.

Example future use case:

```text
create telemetry
create audit log
possibly create alert
commit all together
rollback all if any step fails
```

For now:

```text
API dependency creates session
service calls repository
repository writes data
session commits safely
```

---

## 13. API Versioning Design

API routes will be versioned.

Base path:

```text
/api/v1
```

Examples:

```text
GET /api/v1/health
POST /api/v1/devices
POST /api/v1/telemetry
GET /api/v1/alerts
```

Why versioning?

* supports future breaking changes
* keeps old clients stable
* enterprise API best practice

---

## 14. Naming Standards

### Files

Use lowercase snake_case.

Examples:

```text
device_service.py
device_repository.py
device.py
```

### Classes

Use PascalCase.

Examples:

```text
DeviceService
DeviceRepository
DeviceCreate
DeviceResponse
```

### Functions

Use snake_case.

Examples:

```text
create_device
get_device_by_id
disable_device
```

### Constants

Use uppercase snake case.

Examples:

```text
DEFAULT_PAGE_SIZE
DEVICE_API_KEY_HEADER
```

---

## 15. Testing Design

Testing folders:

```text
tests/unit/
tests/integration/
tests/api/
```

Testing rules:

* Unit tests should test services without real external systems.
* Repository tests may use test database.
* API tests should use FastAPI test client.
* Each requirement should map to at least one test.
* Tests should be deterministic and repeatable.

Example traceability:

```text
FR-001 Register Device
    ↓
DeviceService.create_device()
    ↓
test_create_device_success()
    ↓
test_create_device_duplicate_device_id()
```

---

## 16. Design Patterns Used

## 16.1 Layered Architecture

Used for the overall backend structure.

Reason:

* separates responsibilities
* improves maintainability
* supports testing
* avoids business logic inside routes

---

## 16.2 Service Layer Pattern

Used in:

```text
app/services/
```

Reason:

* keeps business logic in one place
* makes rules testable
* avoids fat API controllers
* supports orchestration across repositories

Example:

```text
DeviceService decides whether a device can be created.
```

---

## 16.3 Repository Pattern

Used in:

```text
app/repositories/
```

Reason:

* isolates database access
* avoids spreading ORM queries everywhere
* makes persistence easier to test or replace
* keeps service logic database-agnostic

Example:

```text
DeviceRepository handles SELECT/INSERT/UPDATE for devices.
```

---

## 16.4 Dependency Injection Pattern

Used in:

```text
app/api/dependencies.py
```

Reason:

* centralizes object creation
* makes testing easier
* allows replacing real services with fake services
* avoids hardcoded dependencies

Example:

```text
API receives DeviceService through Depends().
```

---

## 16.5 DTO / Schema Pattern

Used in:

```text
app/schemas/
```

Reason:

* separates API contracts from database models
* prevents leaking internal fields
* validates request and response data
* improves OpenAPI documentation

Example:

```text
DeviceCreate is not the same as Device database model.
```

---

## 16.6 Middleware Pattern

Used in:

```text
app/core/middleware.py
```

Reason:

* handles cross-cutting concerns
* avoids duplicate logic in every route
* useful for correlation ID, logging, security headers

Example:

```text
CorrelationIdMiddleware runs for every request.
```

---

## 17. Important Backend Rules

The following rules must be followed:

1. API routes must not directly access the database.
2. Business logic must be placed in services.
3. Database queries must be placed in repositories.
4. API schemas must be separate from database models.
5. Configuration must come from environment variables.
6. Secrets must not be committed.
7. All important actions must be logged.
8. Errors must be controlled and consistent.
9. Tests must be added for new features.
10. Code should be formatted, linted, and type-hinted.

---

## 18. Summary

This low-level design defines how the backend will be implemented.

The backend will use layered architecture, service layer pattern, repository pattern, dependency injection, DTO/schema pattern, middleware pattern, structured logging, controlled exceptions, and environment-based configuration.

This design will help us build a backend that is production-ready, maintainable, testable, and suitable for enterprise-level development.