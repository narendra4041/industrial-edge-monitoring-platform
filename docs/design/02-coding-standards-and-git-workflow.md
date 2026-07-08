# Coding Standards and Git Workflow

## Project Name

Industrial Edge Monitoring Platform

## 1. Purpose

This document defines the coding standards, Git workflow, branch strategy, commit message format, pull request rules, and Definition of Done for the Industrial Edge Monitoring Platform.

The goal is to follow enterprise-level software engineering practices from the beginning of the project.

---

## 2. Development Principles

The project will follow these development principles:

* write clean, readable, maintainable code
* keep business logic separate from API routes
* use type hints wherever possible
* write automated tests for important behavior
* avoid hardcoded configuration
* avoid committing secrets
* document important design decisions
* make small, meaningful commits
* keep code production-oriented, not demo-style

---

## 3. Python Coding Standards

## 3.1 Formatting

Python code will be formatted consistently.

Tools:

* Ruff formatter
* Ruff linter

Rules:

* use 4 spaces for indentation
* use snake_case for functions and variables
* use PascalCase for classes
* use uppercase snake case for constants
* keep functions small and focused
* avoid deeply nested logic where possible

Examples:

```python
def create_device(device_id: str) -> None:
    pass
```

```python
class DeviceService:
    pass
```

```python
DEFAULT_PAGE_SIZE = 50
```

---

## 3.2 Type Hints

Use Python type hints for function arguments and return values.

Good:

```python
def get_device(device_id: str) -> DeviceResponse:
    pass
```

Avoid:

```python
def get_device(device_id):
    pass
```

Why:

* improves readability
* helps IDE support
* supports static analysis
* reduces runtime mistakes
* works well with FastAPI and Pydantic

---

## 3.3 Function Design

Functions should do one clear thing.

Good:

```python
def validate_device_status(status: str) -> bool:
    return status in {"ACTIVE", "DISABLED"}
```

Avoid large functions that validate, transform, save, log, and return responses all in one place.

---

## 3.4 Error Handling

Use controlled exceptions.

Rules:

* do not expose internal stack traces to API clients
* services should raise application exceptions
* API exception handlers should convert exceptions into HTTP responses
* unexpected errors should be logged with correlation_id

Example exception types:

```text
NotFoundError
ConflictError
UnauthorizedError
ForbiddenError
ValidationError
```

---

## 3.5 Configuration

Configuration must come from environment variables.

Rules:

* no hardcoded passwords
* no hardcoded API keys
* no production secrets in code
* use `.env` only for local development
* commit `.env.example`, not `.env`

---

## 4. Backend Layering Rules

The backend must follow this dependency flow:

```text
API Layer
    ↓
Service Layer
    ↓
Repository Layer
    ↓
Database Model Layer
```

Allowed:

```text
API calls Service
Service calls Repository
Repository uses Database Model
```

Not allowed:

```text
API directly queries database
Repository calls Service
Database Model imports API code
Service returns raw HTTP responses
```

---

## 5. Design Patterns to Follow

## 5.1 Service Layer Pattern

Business logic should live in service classes.

Example:

```text
DeviceService.create_device()
TelemetryService.ingest_telemetry()
AlertService.acknowledge_alert()
```

Why:

* keeps API routes clean
* makes business rules testable
* avoids duplicate logic
* improves maintainability

---

## 5.2 Repository Pattern

Database operations should live in repository classes.

Example:

```text
DeviceRepository.get_by_device_id()
DeviceRepository.create()
DeviceRepository.disable()
```

Why:

* isolates persistence logic
* avoids spreading SQLAlchemy queries across the project
* makes testing easier
* allows database implementation changes later

---

## 5.3 Dependency Injection

Dependencies should be provided using FastAPI dependency functions.

Example:

```text
get_db_session()
get_device_repository()
get_device_service()
```

Why:

* avoids hardcoded dependencies
* improves testing
* supports replacing real objects with test doubles
* centralizes object creation

---

## 5.4 DTO / Schema Pattern

API request and response models should use Pydantic schemas.

Example:

```text
DeviceCreate
DeviceUpdate
DeviceResponse
```

Why:

* separates API contract from database model
* validates input
* controls response shape
* improves OpenAPI documentation

---

## 6. Git Branch Strategy

The project will use a simple enterprise-style branch strategy.

Main branches:

```text
main
develop
```

Feature branches:

```text
feature/*
```

Bugfix branches:

```text
bugfix/*
```

Hotfix branches:

```text
hotfix/*
```

Release branches:

```text
release/*
```

Examples:

```text
feature/backend-foundation
feature/device-registry
feature/telemetry-ingestion
feature/linux-edge-agent
feature/alert-engine
feature/observability
bugfix/device-duplicate-validation
hotfix/security-header-fix
```

---

## 7. Branch Rules

## 7.1 main Branch

The `main` branch represents stable production-ready code.

Rules:

* no direct commits to main
* changes should come through pull requests
* CI must pass before merge
* main should always be deployable

## 7.2 develop Branch

The `develop` branch represents active integration work.

Rules:

* feature branches merge into develop
* develop should remain stable
* CI should run before merging

## 7.3 feature Branches

Feature branches are used for new functionality.

Example:

```bash
git checkout -b feature/device-registry
```

Rules:

* one feature per branch
* small commits
* tests added
* documentation updated if needed

---

## 8. Commit Message Standard

Use Conventional Commit style.

Format:

```text
<type>: <short description>
```

Common types:

| Type     | Purpose                                    |
| -------- | ------------------------------------------ |
| feat     | New feature                                |
| fix      | Bug fix                                    |
| docs     | Documentation change                       |
| test     | Test change                                |
| refactor | Code restructuring without behavior change |
| chore    | Tooling, setup, maintenance                |
| ci       | CI/CD changes                              |
| perf     | Performance improvement                    |
| security | Security improvement                       |

Examples:

```text
docs: add backend low-level design
feat: add health check endpoints
feat: add device registry service
test: add device creation tests
fix: prevent duplicate device registration
chore: configure ruff and pytest
ci: add backend test workflow
```

---

## 9. Pull Request Checklist

Every pull request should check:

```text
Code compiles successfully
Tests added or updated
All tests pass locally
Linting passes
No secrets committed
Documentation updated if needed
Requirement ID mentioned where applicable
Design pattern followed correctly
Error handling added
Logging added where useful
```

Example PR description:

```text
## Summary

Adds device registry API for registering and viewing devices.

## Requirement

FR-001 Register Device
FR-002 View Device

## Design

Uses Service Layer Pattern and Repository Pattern.

## Testing

- test_create_device_success
- test_create_device_duplicate_id
- test_get_device_not_found
```

---

## 10. Definition of Done

A feature is considered done only when:

* code is implemented
* code follows layered architecture
* business logic is in service layer
* database access is in repository layer
* request and response schemas are created
* error handling is added
* tests are added
* tests pass
* documentation is updated if needed
* no secrets are committed
* CI pipeline passes
* feature can be explained clearly

---

## 11. Code Review Guidelines

During review, check:

* Is the code readable?
* Is the logic in the correct layer?
* Are names clear?
* Are errors handled properly?
* Are tests meaningful?
* Is there duplicated code?
* Are design patterns used correctly?
* Is the feature over-engineered or under-engineered?
* Are security concerns handled?
* Are logs useful but not exposing secrets?

---

## 12. Testing Expectations

Each important feature should have tests.

Minimum testing expectations:

```text
Unit tests for service logic
API tests for routes
Integration tests for database flows where needed
Security tests for protected endpoints
```

Example mapping:

```text
FR-001 Register Device
    ↓
test_create_device_success
test_create_device_duplicate_device_id
test_create_device_invalid_payload
```

---

## 13. Security Coding Rules

Rules:

* never commit `.env`
* never log passwords, API keys, JWT tokens, or secrets
* validate all external input
* use role checks for protected operations
* use parameterized ORM queries
* return generic messages for unexpected errors
* keep dependencies updated
* run security scans in CI later

---

## 14. Documentation Rules

Documentation should be updated when:

* a new API is added
* a new design decision is made
* a new environment variable is added
* a new component is introduced
* deployment steps change
* production support behavior changes

Documentation locations:

```text
docs/requirements/
docs/architecture/
docs/design/
docs/testing/
docs/deployment/
docs/runbooks/
```

---

## 15. Local Development Workflow

Typical workflow:

```bash
git checkout develop
git pull
git checkout -b feature/device-registry
```

Make changes.

Run tests:

```bash
pytest
```

Run linting later:

```bash
ruff check .
```

Commit:

```bash
git add .
git commit -m "feat: add device registry foundation"
```

Push:

```bash
git push origin feature/device-registry
```

Create pull request into `develop`.

---

## 16. Summary

This project will follow enterprise-style coding and Git practices.

The key goals are clean code, small commits, clear branch strategy, requirement traceability, automated testing, secure development, and maintainable architecture.