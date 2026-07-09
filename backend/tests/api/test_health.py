from fastapi.testclient import TestClient

from app.main import create_app


def test_health_check_returns_healthy() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_liveness_check_returns_alive() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_check_returns_ready() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
