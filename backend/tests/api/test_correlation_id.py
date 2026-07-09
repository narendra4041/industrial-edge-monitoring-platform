from fastapi.testclient import TestClient

from app.core.middleware import CORRELATION_ID_HEADER
from app.main import create_app


def test_correlation_id_is_generated_when_missing() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert CORRELATION_ID_HEADER in response.headers
    assert response.headers[CORRELATION_ID_HEADER] != ""


def test_existing_correlation_id_is_reused() -> None:
    client = TestClient(create_app())

    correlation_id = "test-correlation-id-123"

    response = client.get(
        "/api/v1/health",
        headers={CORRELATION_ID_HEADER: correlation_id},
    )

    assert response.status_code == 200
    assert response.headers[CORRELATION_ID_HEADER] == correlation_id
