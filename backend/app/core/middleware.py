from collections.abc import Callable
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


CORRELATION_ID_HEADER = "X-Correlation-ID"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Ensure every request has a correlation ID.

    If the client sends X-Correlation-ID, we reuse it.
    If not, we generate a new UUID.

    The correlation ID is stored in request.state and returned in the response header.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        correlation_id = request.headers.get(CORRELATION_ID_HEADER)

        if not correlation_id:
            correlation_id = str(uuid4())

        request.state.correlation_id = correlation_id

        response = await call_next(request)
        response.headers[CORRELATION_ID_HEADER] = correlation_id

        return response