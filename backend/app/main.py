import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.v1.api_router import api_router
from app.core.config import get_settings
from app.core.exception_handlers import (
    application_error_handler,
    request_validation_error_handler,
    unhandled_exception_handler,
)
from app.core.exceptions import ApplicationError
from app.core.logging import setup_logging
from app.core.middleware import (
    CorrelationIdMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)

    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    logger.info(
        "Application started",
        extra={
            "service_name": settings.app_name,
            "environment": settings.app_env,
        },
    )

    return app


app = create_app()