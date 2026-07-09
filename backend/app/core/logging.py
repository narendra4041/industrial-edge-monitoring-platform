import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any


class JsonLogFormatter(logging.Formatter):
    """Format log records as JSON for production-style observability."""

    def format(self, record: logging.LogRecord) -> str:
        log_record: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        extra_fields = [
            "service_name",
            "environment",
            "correlation_id",
            "request_method",
            "request_path",
            "status_code",
            "duration_ms",
        ]

        for field in extra_fields:
            value = getattr(record, field, None)
            if value is not None:
                log_record[field] = value

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, default=str)


def setup_logging(log_level: str = "INFO") -> None:
    """Configure root logger with JSON logs.

    Only remove previously added application JSON handlers.
    Do not clear all handlers because test frameworks like pytest caplog
    attach their own handlers to capture logs.
    """

    normalized_level = log_level.upper()
    level = getattr(logging, normalized_level, logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    for existing_handler in list(root_logger.handlers):
        if getattr(existing_handler, "_industrial_edge_json_handler", False):
            root_logger.removeHandler(existing_handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonLogFormatter())
    handler._industrial_edge_json_handler = True  # type: ignore[attr-defined]

    root_logger.addHandler(handler)

    logging.getLogger("uvicorn.access").disabled = True