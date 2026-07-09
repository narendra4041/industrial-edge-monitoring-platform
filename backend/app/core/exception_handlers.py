import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ApplicationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


logger = logging.getLogger(__name__)


def _get_correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _error_response(
    status_code: int,
    error_code: str,
    message: str,
    correlation_id: str | None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error_code": error_code,
            "message": message,
            "correlation_id": correlation_id,
        },
    )


async def application_error_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    correlation_id = _get_correlation_id(request)

    status_code = 500

    if isinstance(exc, ValidationError):
        status_code = 422
    elif isinstance(exc, NotFoundError):
        status_code = 404
    elif isinstance(exc, ConflictError):
        status_code = 409
    elif isinstance(exc, UnauthorizedError):
        status_code = 401
    elif isinstance(exc, ForbiddenError):
        status_code = 403

    logger.warning(
        "Application error occurred",
        extra={
            "correlation_id": correlation_id,
            "request_method": request.method,
            "request_path": request.url.path,
            "status_code": status_code,
            "error_code": exc.error_code,
        },
    )

    return _error_response(
        status_code=status_code,
        error_code=exc.error_code,
        message=exc.message,
        correlation_id=correlation_id,
    )


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    correlation_id = _get_correlation_id(request)

    logger.warning(
        "Request validation error occurred",
        extra={
            "correlation_id": correlation_id,
            "request_method": request.method,
            "request_path": request.url.path,
            "status_code": 422,
            "error_code": "REQUEST_VALIDATION_ERROR",
        },
    )

    return _error_response(
        status_code=422,
        error_code="REQUEST_VALIDATION_ERROR",
        message="Request validation failed",
        correlation_id=correlation_id,
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    correlation_id = _get_correlation_id(request)

    logger.exception(
        "Unhandled exception occurred",
        extra={
            "correlation_id": correlation_id,
            "request_method": request.method,
            "request_path": request.url.path,
            "status_code": 500,
            "error_code": "INTERNAL_SERVER_ERROR",
        },
    )

    return _error_response(
        status_code=500,
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred",
        correlation_id=correlation_id,
    )