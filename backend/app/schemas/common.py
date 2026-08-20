"""
Common API response schemas.
"""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard API error response."""

    detail: str


class MessageResponse(BaseModel):
    """Standard API message response."""

    message: str
