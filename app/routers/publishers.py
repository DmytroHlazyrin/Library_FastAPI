from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Publisher, PublisherCreate
from app.crud import create_publisher, get_publisher, get_publishers
from app.dependencies import get_db, admin_required
from db import models

router = APIRouter()

# ------------------------------------
# Endpoints for Publishers
# ------------------------------------


@router.post("/publishers/", response_model=Publisher)
async def create_publisher_endpoint(
    publisher: PublisherCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(admin_required),
) -> Publisher:
    """Create a new publisher."""
    return create_publisher(db=db, publisher=publisher)


@router.get("/publishers/", response_model=list[Publisher])
async def get_publishers_endpoint(
    offset: int = 0,
    limit: int = 10,
    sort_by: str = "name",
    sort_order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
) -> list[Publisher]:
    """Retrieve a list of publishers with pagination."""
    return get_publishers(
        db=db,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/publishers/{publisher_id}", response_model=Publisher)
async def get_publisher_endpoint(
    publisher_id: int, db: Session = Depends(get_db)
) -> Publisher:
    """Retrieve a publisher by its ID."""
    db_publisher = get_publisher(db=db, publisher_id=publisher_id)
    if db_publisher is None:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return db_publisher
