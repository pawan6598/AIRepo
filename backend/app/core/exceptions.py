"""Custom exception hierarchy."""
from __future__ import annotations

from typing import Any


class ApplicationError(Exception):
    """Base application exception."""

    def __init__(self, message: str, *, payload: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.payload = payload or {}


class ValidationError(ApplicationError):
    """Raised for input validation errors."""


class ExternalServiceError(ApplicationError):
    """Raised when external service fails."""


class NotFoundError(ApplicationError):
    """Raised when entity not found."""
