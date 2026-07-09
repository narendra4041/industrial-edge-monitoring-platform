class ApplicationError(Exception):
    """Base exception for controlled application errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "APPLICATION_ERROR",
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class ValidationError(ApplicationError):
    """Raised when business validation fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "VALIDATION_ERROR",
    ) -> None:
        super().__init__(message=message, error_code=error_code)


class NotFoundError(ApplicationError):
    """Raised when a requested resource does not exist."""

    def __init__(
        self,
        message: str,
        error_code: str = "NOT_FOUND",
    ) -> None:
        super().__init__(message=message, error_code=error_code)


class ConflictError(ApplicationError):
    """Raised when a resource conflict occurs."""

    def __init__(
        self,
        message: str,
        error_code: str = "CONFLICT",
    ) -> None:
        super().__init__(message=message, error_code=error_code)


class UnauthorizedError(ApplicationError):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "UNAUTHORIZED",
    ) -> None:
        super().__init__(message=message, error_code=error_code)


class ForbiddenError(ApplicationError):
    """Raised when authorization fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "FORBIDDEN",
    ) -> None:
        super().__init__(message=message, error_code=error_code)