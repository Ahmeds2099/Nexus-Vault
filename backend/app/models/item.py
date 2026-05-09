"""
models/item.py — SQLAlchemy ORM model for the Item table.

This class defines what the 'items' table looks like in PostgreSQL.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Item(Base):
    """
    The core data model — represents a single piece of saved content.
    MVP v2 fields support the Universal Share Capture flow.
    """

    __tablename__ = "items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )

    # ── Intake Fields ─────────────────────────────────────────────────────
    raw_url = Column(
        String(2048),
        nullable=True,
        comment="The original URL or text captured via share sheet",
    )
    
    # ── Extracted Content Fields ──────────────────────────────────────────
    title = Column(
        String(500),
        nullable=True,
        comment="Title of the saved item (can be extracted later)",
    )

    description = Column(
        Text,
        nullable=True,
        comment="Short description or excerpt of the content",
    )

    thumbnail = Column(
        String(2048),
        nullable=True,
        comment="Preview image URL for the item",
    )
    
    source = Column(
        String(255),
        nullable=True,
        index=True,
        comment="Detected source platform (e.g., YouTube, GitHub, Web)",
    )

    # ── Organization Fields ───────────────────────────────────────────────
    item_type = Column(
        String(100),
        nullable=False,
        default="link",
        index=True,
        comment="Deterministic type: article, video, tool, note, link, pdf",
    )
    
    category = Column(
        String(100),
        nullable=False,
        default="Read Later",
        index=True,
        comment="User categorization folder (Read Later, Important, etc.)",
    )

    is_read = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
    )

    # ── Processing & Metadata ─────────────────────────────────────────────
    metadata_json = Column(
        JSON,
        nullable=True,
        default={},
        comment="Raw OpenGraph, Twitter Card, or scraped JSON data",
    )

    processing_status = Column(
        String(50),
        nullable=False,
        default="pending",
        index=True,
        comment="pending | completed | failed",
    )

    # ── Timestamps ────────────────────────────────────────────────────────
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f"<Item id={self.id} title='{self.title}' type='{self.item_type}'>"
