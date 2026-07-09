from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error_code: str = Field(..., examples=["DEVICE_NOT_FOUND"])
    message: str = Field(..., examples=["Device was not found"])
    correlation_id: str | None = Field(default=None, examples=["abc-123"])