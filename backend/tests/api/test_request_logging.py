import logging

from fastapi.testclient import TestClient

from app.core.middleware import CORRELATION_ID_HEADER
from app.main import create_app


def test_request_logging_includes_request_details(caplog) -> None:
    client = TestClient(create_app())

    correlation_id = "request-log-test-id"

    with caplog.at_level(logging.INFO):
        response = client.get(
            "/api/v1/health",
            headers={CORRELATION_ID_HEADER: correlation_id},
        )

    assert response.status_code == 200

    matching_logs = [
        record
        for record in caplog.records
        if record.getMessage() == "HTTP request completed"
    ]

    assert len(matching_logs) == 1

    log_record = matching_logs[0]

    assert log_record.correlation_id == correlation_id
    assert log_record.request_method == "GET"
    assert log_record.request_path == "/api/v1/health"
    assert log_record.status_code == 200
    assert log_record.duration_ms >= 0