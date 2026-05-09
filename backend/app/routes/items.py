"""
routes/items.py — HTTP route handlers for the /api/items endpoints.

Responsibilities:
- Accept and validate HTTP requests (Pydantic does this automatically)
- Call the appropriate service function
- Return properly formatted HTTP responses
- Handle HTTP-level errors (404, 400, etc.)

Does NOT contain business logic — that lives in item_service.py
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ApiResponse,
    ItemListResponse,
)
from app.services.item_service import ItemService

router = APIRouter(prefix="/api/items", tags=["Items"])


# ── POST /api/items ────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Save a new piece of content (URL, note, article, etc.)",
)
def create_item(
    payload: ItemCreate,
    db: Session = Depends(get_db),
):
    """Create and persist a new item to the database."""
    item = ItemService.create(db=db, payload=payload)
    return ApiResponse(
        success=True,
        data=ItemResponse.model_validate(item),
    )


# ── GET /api/items ─────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=ItemListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all items",
    description="Retrieve all saved items, with optional filters by category, type, or status.",
)
def list_items(
    category: Optional[str] = Query(
        default=None,
        description="Filter by user category (Read Later, Important, etc.)",
    ),
    item_type: Optional[str] = Query(
        default=None,
        description="Filter by content type (article, video, tool, note, link, pdf)",
    ),
    is_read: Optional[bool] = Query(
        default=None,
        description="Filter by read status (true/false)",
    ),
    processing_status: Optional[str] = Query(
        default=None,
        description="Filter by status (pending, completed, failed)",
    ),
    skip: int = Query(default=0, ge=0, description="Pagination offset"),
    limit: int = Query(default=100, ge=1, le=500, description="Max items to return"),
    db: Session = Depends(get_db),
):
    """Retrieve items with optional filtering and pagination."""
    items, total = ItemService.get_all(
        db=db,
        category=category,
        item_type=item_type,
        is_read=is_read,
        processing_status=processing_status,
        skip=skip,
        limit=limit,
    )
    return ItemListResponse(
        success=True,
        data=[ItemResponse.model_validate(item) for item in items],
        total=total,
    )


# ── GET /api/items/{id} ────────────────────────────────────────────────────────

@router.get(
    "/{item_id}",
    response_model=ApiResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a single item",
    description="Retrieve a specific item by its UUID.",
)
def get_item(
    item_id: UUID,
    db: Session = Depends(get_db),
):
    """Fetch a single item by UUID. Returns 404 if not found."""
    item = ItemService.get_by_id(db=db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )
    return ApiResponse(
        success=True,
        data=ItemResponse.model_validate(item),
    )


# ── PATCH /api/items/{id} ──────────────────────────────────────────────────────

@router.patch(
    "/{item_id}",
    response_model=ApiResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an item",
    description="Partially update an item — only provided fields are changed.",
)
def update_item(
    item_id: UUID,
    payload: ItemUpdate,
    db: Session = Depends(get_db),
):
    """
    PATCH — partial update.
    Only fields included in the request body will be changed.
    Fields not included are left as-is.
    """
    item = ItemService.get_by_id(db=db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )

    # Check that at least one field was provided
    if not payload.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update",
        )

    updated_item = ItemService.update(db=db, item=item, payload=payload)
    return ApiResponse(
        success=True,
        data=ItemResponse.model_validate(updated_item),
    )


# ── DELETE /api/items/{id} ─────────────────────────────────────────────────────

@router.delete(
    "/{item_id}",
    response_model=ApiResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete an item",
    description="Permanently remove an item from the vault.",
)
def delete_item(
    item_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete an item by UUID. Returns 404 if not found."""
    item = ItemService.get_by_id(db=db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )

    ItemService.delete(db=db, item=item)
    return ApiResponse(
        success=True,
        data={"message": f"Item '{item_id}' deleted successfully"},
    )
