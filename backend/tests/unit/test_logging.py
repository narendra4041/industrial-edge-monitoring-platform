import json
import logging

from app.core.logging import JsonLogFormatter, setup_logging


def test_json_log_formatter_outputs_expected_fields() -> None:
    formatter = JsonLogFormatter()

    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    parsed_output = json.loads(output)

    assert parsed_output["level"] == "INFO"
    assert parsed_output["logger"] == "test_logger"
    assert parsed_output["message"] == "Test message"
    assert "timestamp" in parsed_output
    assert "module" in parsed_output
    assert "function" in parsed_output
    assert "line" in parsed_output


def test_json_log_formatter_includes_extra_fields() -> None:
    formatter = JsonLogFormatter()

    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=20,
        msg="Request completed",
        args=(),
        exc_info=None,
    )

    record.correlation_id = "test-correlation-id"
    record.request_method = "GET"
    record.request_path = "/api/v1/health"
    record.status_code = 200
    record.duration_ms = 12.5

    output = formatter.format(record)
    parsed_output = json.loads(output)

    assert parsed_output["correlation_id"] == "test-correlation-id"
    assert parsed_output["request_method"] == "GET"
    assert parsed_output["request_path"] == "/api/v1/health"
    assert parsed_output["status_code"] == 200
    assert parsed_output["duration_ms"] == 12.5


def test_setup_logging_configures_root_logger() -> None:
    setup_logging("DEBUG")

    root_logger = logging.getLogger()

    assert root_logger.level == logging.DEBUG
    assert len(root_logger.handlers) == 1