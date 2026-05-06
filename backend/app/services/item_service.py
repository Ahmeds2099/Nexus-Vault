"""
services/item_service.py — All business logic for Item CRUD operations.

Rules:
- Services NEVER handle HTTP (no Request/Response objects here)
- Services NEVER know about FastAPI — only Python + SQLAlchemy
- Routes call Services; Services call the DB
- This makes services easily testable in isolation
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """
    Service class for all Item database operations.
    Each method is a clean, single-responsibility function.
    """

    @staticmethod
    def create(db: Session, payload: ItemCreate) -> Item:
        """
        Insert a new item into the database.
        
        Args:
            db: Active database session (injected by FastAPI)
            payload: Validated ItemCreate data from the request
        
        Returns:
            The newly created Item ORM object (with id and timestamps set)
        """
        item = Item(
            title=payload.title,
            url=payload.url,
            description=payload.description,
            thumbnail_url=payload.thumbnail_url,
            category=payload.category,
            is_read=payload.is_read,
        )
        db.add(item)
        db.commit()
        db.refresh(item)  # Reload from DB to get generated id, created_at, etc.
        return item

    @staticmethod
    def get_all(
        db: Session,
        category: Optional[str] = None,
        is_read: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Item], int]:
        """
        Fetch all items with optional filters.
        
        Args:
            db: Active database session
            category: Filter by category (e.g. "read_later", "video")
            is_read: Filter by read status (True/False)
            skip: Pagination offset (default 0)
            limit: Max items to return (default 100)
        
        Returns:
            Tuple of (list of Item objects, total count before pagination)
        """
        query = db.query(Item)

        # Build dynamic filters
        filters = []
        if category is not None:
            filters.append(Item.category == category)
        if is_read is not None:
            filters.append(Item.is_read == is_read)

        if filters:
            query = query.filter(and_(*filters))

        # Get total count before applying pagination
        total = query.count()

        # Apply ordering and pagination
        items = (
            query
            .order_by(Item.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return items, total

    @staticmethod
    def get_by_id(db: Session, item_id: UUID) -> Optional[Item]:
        """
        Fetch a single item by its UUID.
        
        Returns None if not found (route layer handles the 404).
        """
        return db.query(Item).filter(Item.id == item_id).first()

    @staticmethod
    def update(db: Session, item: Item, payload: ItemUpdate) -> Item:
        """
        Partially update an existing item (PATCH semantics).
        
        Only fields that are provided (not None) in the payload will be updated.
        This is true PATCH behaviour — unset fields remain unchanged.
        
        Args:
            db: Active database session
            item: The Item ORM object to update (already fetched from DB)
            payload: Validated ItemUpdate data (partial)
        
        Returns:
            The updated Item ORM object
        """
        # model_dump(exclude_unset=True) returns only fields the client sent
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(item, field, value)

        # Manually set updated_at in case the DB trigger is slow
        item.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, item: Item) -> None:
        """
        Permanently delete an item from the database.
        
        Args:
            db: Active database session
            item: The Item ORM object to delete
        """
        db.delete(item)
        db.commit()
