"""Security utilities for JWT handling."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict

import jwt

from .config import settings

ALGORITHM = "HS256"


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token for a subject."""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode: Dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode a JWT token."""
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
