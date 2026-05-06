"""
schemas/item.py — Pydantic schemas for API request/response validation.

Schemas are NOT the same as models:
- Models = what's stored in the database (SQLAlchemy)
- Schemas = what's accepted/returned by the API (Pydantic)

This separation lets us control exactly what data is exposed via the API,
independent of what's stored in the DB.
"""

from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, HttpUrl, field_validator, ConfigDict


# ── Valid Categories ───────────────────────────────────────────────────────────
VALID_CATEGORIES = {"read_later", "article", "video", "tool", "note"}


# ── Request Schemas (what the API accepts) ─────────────────────────────────────

class ItemCreate(BaseModel):
    """Schema for creating a new item. Required: title. All others optional."""

    title: str
    url: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category: str = "read_later"
    is_read: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty")
        if len(v) > 500:
            raise ValueError("Title must be 500 characters or fewer")
        return v

    @field_validator("category")
    @classmethod
    def category_must_be_valid(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category '{v}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
            )
        return v


class ItemUpdate(BaseModel):
    """
    Schema for partial updates (PATCH).
    All fields are optional — only provided fields will be updated.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_read: Optional[bool] = None
    thumbnail_url: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty")
            if len(v) > 500:
                raise ValueError("Title must be 500 characters or fewer")
        return v

    @field_validator("category")
    @classmethod
    def category_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            if v not in VALID_CATEGORIES:
                raise ValueError(
                    f"Invalid category '{v}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
                )
        return v


# ── Response Schemas (what the API returns) ────────────────────────────────────

class ItemResponse(BaseModel):
    """Schema for a single item in API responses."""

    id: UUID
    title: str
    url: Optional[str]
    description: Optional[str]
    thumbnail_url: Optional[str]
    category: str
    is_read: bool
    created_at: datetime
    updated_at: datetime

    # Allows Pydantic to read data from SQLAlchemy model attributes
    model_config = ConfigDict(from_attributes=True)


# ── Wrapper Response Format ────────────────────────────────────────────────────
# All API responses follow: { "success": true/false, "data": ..., "error": ... }

class ApiResponse(BaseModel):
    """Standard wrapper for all API responses."""
    success: bool
    data: Any = None
    error: Optional[str] = None


class ItemListResponse(BaseModel):
    """Response wrapper for a list of items with count metadata."""
    success: bool
    data: list[ItemResponse]
    total: int
    error: Optional[str] = None
