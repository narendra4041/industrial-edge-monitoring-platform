from typing import Annotated

from fastapi import Body
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.core.middleware import CORRELATION_ID_HEADER
from app.main import create_app


class SamplePayload(BaseModel):
    name: str


def test_not_found_error_returns_standard_error_response() -> None:
    app = create_app()

    @app.get("/test/not-found")
    def raise_not_found() -> None:
        raise NotFoundError(message="Device was not found", error_code="DEVICE_NOT_FOUND")

    client = TestClient(app)

    response = client.get(
        "/test/not-found",
        headers={CORRELATION_ID_HEADER: "error-test-001"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "error_code": "DEVICE_NOT_FOUND",
        "message": "Device was not found",
        "correlation_id": "error-test-001",
    }


def test_conflict_error_returns_standard_error_response() -> None:
    app = create_app()

    @app.get("/test/conflict")
    def raise_conflict() -> None:
        raise ConflictError(message="Device already exists", error_code="DEVICE_ALREADY_EXISTS")

    client = TestClient(app)

    response = client.get(
        "/test/conflict",
        headers={CORRELATION_ID_HEADER: "error-test-002"},
    )

    assert response.status_code == 409
    assert response.json() == {
        "error_code": "DEVICE_ALREADY_EXISTS",
        "message": "Device already exists",
        "correlation_id": "error-test-002",
    }


def test_business_validation_error_returns_standard_error_response() -> None:
    app = create_app()

    @app.get("/test/validation")
    def raise_validation() -> None:
        raise ValidationError(message="Invalid device status", error_code="INVALID_DEVICE_STATUS")

    client = TestClient(app)

    response = client.get(
        "/test/validation",
        headers={CORRELATION_ID_HEADER: "error-test-003"},
    )

    assert response.status_code == 422
    assert response.json() == {
        "error_code": "INVALID_DEVICE_STATUS",
        "message": "Invalid device status",
        "correlation_id": "error-test-003",
    }


def test_request_validation_error_returns_standard_error_response() -> None:
    app = create_app()

    @app.post("/test/request-validation")
    def validate_payload(payload: Annotated[SamplePayload, Body()]) -> dict[str, str]:
        return {"name": payload.name}

    client = TestClient(app)

    response = client.post(
        "/test/request-validation",
        json={},
        headers={CORRELATION_ID_HEADER: "error-test-004"},
    )

    assert response.status_code == 422
    assert response.json() == {
        "error_code": "REQUEST_VALIDATION_ERROR",
        "message": "Request validation failed",
        "correlation_id": "error-test-004",
    }
