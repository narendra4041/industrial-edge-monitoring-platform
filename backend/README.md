# Industrial Edge Backend API

## Overview
This service is currently in Milestone 1 backend foundation development.

This is the backend API service for the Industrial Edge Monitoring Platform.

The backend is built using Python and FastAPI and follows production-oriented backend engineering practices such as layered architecture, structured configuration, JSON logging, correlation IDs, request logging, global exception handling, security headers, automated tests, and Docker-based execution.

---

## Current Backend Capabilities

Implemented in Milestone 1:

- FastAPI application foundation
- Application Factory Pattern
- API versioning with `/api/v1`
- Health endpoint
- Liveness endpoint
- Readiness endpoint
- Structured application configuration
- JSON logging
- Correlation ID middleware
- Request logging middleware
- Global exception handling
- Security headers middleware
- Dockerfile
- Docker Compose support with TimescaleDB
- Unit and API tests

---

## Architecture Style

The backend follows layered architecture.

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

Current Milestone 1 focuses on foundation-level backend infrastructure.

Future milestones will add:

- Device registry
- Telemetry ingestion
- Quarantine module
- Alert engine
- Authentication and authorization
- Database models and migrations
- Observability metrics and tracing

---

## Design Patterns Used

### Application Factory Pattern

The FastAPI application is created using:

```python
def create_app() -> FastAPI:
    ...
```

This supports testing, configuration, middleware registration, and future environment-specific initialization.

### Modular Router Pattern

API routes are separated into router modules.

Current router:

```text
app/api/v1/routers/health.py
```

Future routers:

```text
devices.py
telemetry.py
alerts.py
auth.py
```

### Configuration Object Pattern

Application settings are centralized in:

```text
app/core/config.py
```

This avoids scattered `os.getenv()` calls across the codebase.

### Facade Pattern for Logging

Logging setup is centralized in:

```text
app/core/logging.py
```

The application calls one simple function:

```python
setup_logging(settings.log_level)
```

This hides lower-level logging configuration details.

### Middleware Pattern

Middleware is used for cross-cutting concerns:

- correlation ID
- request logging
- security headers

Location:

```text
app/core/middleware.py
```

### Custom Exception Pattern

Application-specific exceptions are defined in:

```text
app/core/exceptions.py
```

### Centralized Exception Handler Pattern

Exception-to-response mapping is handled in:

```text
app/core/exception_handlers.py
```

This ensures consistent API error responses.

---

## Local Development Setup

### 1. Create virtual environment

From the `backend/` folder:

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate on Git Bash / Linux / macOS:

```bash
source .venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -e ".[dev]"
```

---

### 3. Run tests

```bash
pytest -q
```

Expected result:

```text
16 passed
```

The exact number may increase as new features are added.

---

### 4. Run the API locally

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/api/v1/health
http://localhost:8000/docs
```

---

## API Endpoints

### Health Check

```http
GET /api/v1/health
```

Response:

```json
{
  "status": "healthy"
}
```

### Liveness Check

```http
GET /api/v1/live
```

Response:

```json
{
  "status": "alive"
}
```

### Readiness Check

```http
GET /api/v1/ready
```

Response:

```json
{
  "status": "ready"
}
```

---

## Docker Build

From the project root:

```bash
docker build -t industrial-edge-backend:local backend
```

---

## Docker Compose

From the project root:

```bash
docker compose -f infrastructure/docker-compose/docker-compose.yml up --build
```

Open:

```text
http://localhost:8000/api/v1/health
http://localhost:8000/docs
```

Stop containers:

```bash
docker compose -f infrastructure/docker-compose/docker-compose.yml down
```

Stop containers and remove database volume:

```bash
docker compose -f infrastructure/docker-compose/docker-compose.yml down -v
```

---

## Environment Variables

Example configuration is available in:

```text
.env.example
```

Current variables:

| Variable | Purpose |
|---|---|
| APP_NAME | Application display name |
| APP_ENV | Runtime environment |
| API_V1_PREFIX | API version prefix |
| LOG_LEVEL | Logging level |
| DATABASE_URL | Database connection URL |
| JWT_SECRET_KEY | JWT signing secret |
| JWT_ALGORITHM | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | Access token expiry |
| DEVICE_API_KEY_HEADER | Header used for device API key |
| ENABLE_METRICS | Enables metrics later |
| ENABLE_TRACING | Enables tracing later |

Do not commit real `.env` files.

---

## Logging

The backend uses JSON-style structured logs.

Example log fields:

```json
{
  "timestamp": "2026-07-09T13:11:04.524347+00:00",
  "level": "INFO",
  "logger": "app.core.middleware",
  "message": "HTTP request completed",
  "correlation_id": "request-log-test-id",
  "request_method": "GET",
  "request_path": "/api/v1/health",
  "status_code": 200,
  "duration_ms": 3.75
}
```

---

## Correlation ID

Every API response includes:

```text
X-Correlation-ID
```

If the client sends this header, the backend reuses it.

If the client does not send it, the backend generates one.

Example:

```bash
curl -i -H "X-Correlation-ID: local-test-001" http://localhost:8000/api/v1/health
```

---

## Security Headers

Every API response includes basic security headers:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Referrer-Policy: no-referrer
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

---

## Error Response Format

Controlled application errors use this standard format:

```json
{
  "error_code": "DEVICE_NOT_FOUND",
  "message": "Device was not found",
  "correlation_id": "abc-123"
}
```

Unhandled errors return a generic message to avoid leaking internal implementation details.

---

## Code Quality

Current tools:

- pytest
- ruff
- mypy

Run tests:

```bash
pytest -q
```

Run linting:

```bash
ruff check .
```

Run formatting check:

```bash
ruff format --check .
```

Run type checks:

```bash
mypy app tests
```

---

## Notes for Future Milestones

Next backend milestones will introduce:

- SQLAlchemy
- Alembic
- database session management
- repository pattern implementation
- device registry APIs
- telemetry ingestion APIs
- authentication and authorization
- alert engine
- observability metrics