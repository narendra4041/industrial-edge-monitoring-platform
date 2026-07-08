# ADR-002: Use Layered Architecture for Backend

## Status

Accepted

## Date

2026-07-08

## Context

The backend will contain APIs, validation, business logic, database access, authentication, telemetry ingestion, alerting, and audit logging.

If all logic is placed directly inside API endpoints, the code will become difficult to test, maintain, and extend.

The backend needs a clear architecture that separates responsibilities.

## Decision

We will use a layered architecture inspired by Clean Architecture principles.

The backend will be organized into these layers:

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

The expected folder structure will be:

```text
backend/
└── app/
    ├── api/
    ├── core/
    ├── db/
    ├── models/
    ├── repositories/
    ├── schemas/
    ├── services/
    ├── security/
    ├── workers/
    └── main.py
```

## Layer Responsibilities

### API Layer

Responsible for:

* HTTP routes
* request handling
* response handling
* dependency injection
* status codes

The API layer should not contain business logic or direct database queries.

### Schema Layer

Responsible for:

* request models
* response models
* payload validation
* API contracts

We will use Pydantic schemas.

### Service Layer

Responsible for:

* business rules
* orchestration
* validation beyond basic schema validation
* calling repositories
* deciding what should happen

Example:

* create a device
* validate telemetry
* generate alert
* disable device

### Repository Layer

Responsible for:

* database queries
* data persistence
* fetching records
* updating records

The service layer should not directly write SQL or ORM queries.

### Database Model Layer

Responsible for:

* table structure
* ORM models
* relationships
* database constraints

## Design Patterns Used

### Service Layer Pattern

Business logic will live in services instead of API endpoints.

This makes business rules easier to test.

### Repository Pattern

Database access will be hidden behind repository classes or functions.

This makes database logic easier to change and mock during testing.

### Dependency Injection

FastAPI dependencies will provide services, repositories, database sessions, and authentication context.

This makes the application easier to test and extend.

## Alternatives Considered

### Option 1: Simple CRUD structure

API endpoints directly use database models.

Advantages:

* fast to build
* less code initially

Disadvantages:

* poor testability
* business logic spreads across routes
* hard to maintain as project grows
* not production-grade for complex domains

### Option 2: Full Domain-Driven Design

Use entities, aggregates, value objects, domain events, repositories, and application services.

Advantages:

* strong domain modelling
* good for very complex enterprise domains

Disadvantages:

* too heavy for the initial version
* more boilerplate
* slower learning curve

### Option 3: Layered Architecture

Use clear layers with service and repository patterns.

Advantages:

* production-friendly
* easy to understand
* testable
* not too complex
* suitable for portfolio and enterprise-style backend

Disadvantages:

* more files than simple CRUD
* requires discipline to keep layers clean

## Consequences

All backend features must follow the layered structure.

API routes should call services.

Services should call repositories.

Repositories should access database models.

Schemas should define external API contracts.

This decision improves maintainability, testability, and long-term scalability.

## Related Requirements

* NFR-020: Layered Architecture
* NFR-021: Code Quality
* NFR-023: Automated Testing
* NFR-032: Architecture Documentation