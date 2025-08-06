"""Database utilities for metadata storage."""
from __future__ import annotations

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from ..core.config import settings


class MongoService:
    """Simple MongoDB wrapper."""

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.db = self.client.get_default_database()

    async def insert_document(self, data: dict[str, Any]) -> str:
        """Insert document metadata."""
        result = await self.db.documents.insert_one(data)
        return str(result.inserted_id)
