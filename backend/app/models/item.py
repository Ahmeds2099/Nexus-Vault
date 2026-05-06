"""
models/item.py — SQLAlchemy ORM model for the Item table.

This class defines what the 'items' table looks like in PostgreSQL.
Every field here = one column in the database.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Item(Base):
    """
    The core data model — represents a single piece of saved content.
    
    A user can save URLs, notes, articles, etc.
    Each item is categorized and can be marked as read/unread.
    """

    __tablename__ = "items"

    # ── Primary Key ───────────────────────────────────────────────────────
    # UUID instead of integer: safe for offline creation + future multi-user
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        comment="Unique identifier (UUID v4)",
    )

    # ── Core Content Fields ───────────────────────────────────────────────
    title = Column(
        String(500),
        nullable=False,
        comment="Title of the saved item",
    )

    url = Column(
        String(2048),
        nullable=True,
        comment="URL of the saved content (optional for plain notes)",
    )

    description = Column(
        Text,
        nullable=True,
        comment="Short description or excerpt of the content",
    )

    thumbnail_url = Column(
        String(2048),
        nullable=True,
        comment="Preview image URL for the item",
    )

    # ── Organization Fields ───────────────────────────────────────────────
    category = Column(
        String(100),
        nullable=False,
        default="read_later",
        index=True,  # Indexed for fast filtering by category
        comment="Category: read_later | article | video | tool | note",
    )

    is_read = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True,  # Indexed for fast filtering by read status
        comment="Whether the user has read/consumed this item",
    )

    # ── Timestamps ────────────────────────────────────────────────────────
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="When the item was first saved",
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="When the item was last modified",
    )

    def __repr__(self) -> str:
        return f"<Item id={self.id} title='{self.title}' category='{self.category}'>"
