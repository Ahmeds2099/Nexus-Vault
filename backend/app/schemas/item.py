"""
schemas/item.py — Pydantic schemas for API request/response validation.

Updated for MVP v2: Supports Universal Share Capture flow.
"""

from datetime import datetime
from typing import Optional, Any, Dict
from uuid import UUID

from pydantic import BaseModel, HttpUrl, field_validator, ConfigDict, model_validator


# ── Valid Enums ───────────────────────────────────────────────────────────────
VALID_ITEM_TYPES = {"article", "video", "tool", "note", "link", "pdf"}
VALID_STATUSES = {"pending", "completed", "failed"}


# ── Request Schemas (what the API accepts) ────────────────────────────────────

class ItemCreate(BaseModel):
    """
    Schema for creating a new item via Universal Share Capture.
    Clients might only send a raw_url or a block of text (description/title).
    The backend Intake Pipeline will process the rest.
    """
    raw_url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: str = "Read Later"

    @model_validator(mode='after')
    def must_have_content(self):
        if not self.raw_url and not self.title and not self.description:
            raise ValueError("Must provide at least a raw_url, title, or description to capture.")
        return self


class ItemUpdate(BaseModel):
    """
    Schema for partial updates (PATCH).
    """
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    item_type: Optional[str] = None
    is_read: Optional[bool] = None
    thumbnail: Optional[str] = None
    processing_status: Optional[str] = None

    @field_validator("item_type")
    @classmethod
    def item_type_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            if v not in VALID_ITEM_TYPES:
                raise ValueError(
                    f"Invalid item_type '{v}'. Must be one of: {', '.join(sorted(VALID_ITEM_TYPES))}"
                )
        return v

    @field_validator("processing_status")
    @classmethod
    def status_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            if v not in VALID_STATUSES:
                raise ValueError(
                    f"Invalid processing_status '{v}'"
                )
        return v


# ── Response Schemas (what the API returns) ───────────────────────────────────

class ItemResponse(BaseModel):
    """Schema for a single item in API responses."""
    id: UUID
    raw_url: Optional[str]
    title: Optional[str]
    description: Optional[str]
    thumbnail: Optional[str]
    source: Optional[str]
    item_type: str
    category: str
    is_read: bool
    metadata_json: Optional[Dict[str, Any]]
    processing_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Wrapper Response Format ───────────────────────────────────────────────────

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

