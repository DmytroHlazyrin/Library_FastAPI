from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Author, AuthorCreate, Book
from app.crud import create_author, get_author, get_authors, get_author_books
from app.dependencies import get_db, admin_required
from db import models

router = APIRouter()

# ------------------------------------
# Endpoints for Authors
# ------------------------------------


@router.post("/authors/", response_model=Author)
async def create_author_endpoint(
    author: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(admin_required),
) -> Author:
    """Create a new author."""
    return create_author(db=db, author=author)


@router.get("/authors/", response_model=list[Author])
async def get_authors_endpoint(
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    sort_by: Literal["name", "birthdate"] = "name",
    sort_order: Literal["asc", "desc"] = "asc",
) -> list[Author]:
    """Retrieve a list of authors with pagination."""
    return get_authors(
        db=db,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/authors/{author_id}", response_model=Author)
async def get_author_endpoint(
    author_id: int, db: Session = Depends(get_db)
) -> Author:
    """Retrieve an author by their ID."""
    db_author = get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.get("/authors/{author_id}/books", response_model=list[Book])
async def get_author_books_endpoint(
    author_id: int,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
    sort_by: str = "title",
    sort_order: str = "asc",
) -> list[Book]:
    """Retrieve books by an author."""
    author = get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return get_author_books(
        db=db,
        author_id=author_id,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )
