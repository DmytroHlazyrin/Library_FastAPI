from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Genre, GenreCreate, Book
from app.crud import create_genre, get_genre, get_genres, get_genre_books
from app.dependencies import get_db, admin_required
from db import models

router = APIRouter()

# ------------------------------------
# Endpoints for Genres
# ------------------------------------


@router.post("/genres/", response_model=Genre)
async def create_genre_endpoint(
    genre: GenreCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(admin_required),
) -> Genre:
    """Create a new genre."""
    return create_genre(db=db, genre=genre)


@router.get("/genres/", response_model=list[Genre])
async def get_genres_endpoint(
    offset: int = 0,
    limit: int = 10,
    sort_by: str = "name",
    sort_order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
) -> list[Genre]:
    """Retrieve a list of genres with pagination."""
    return get_genres(
        db=db,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/genres/{genre_id}", response_model=Genre)
async def get_genre_endpoint(
    genre_id: int, db: Session = Depends(get_db)
) -> Genre:
    """Retrieve a genre by its ID."""
    db_genre = get_genre(db=db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre


@router.get("/genres/{genre_id}/books", response_model=list[Book])
async def get_author_books_endpoint(
    genre_id: int,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
    sort_by: str = "title",
    sort_order: str = "asc",
) -> list[Book]:
    """Retrieve books by an author."""
    genre = get_genre(db=db, genre_id=genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return get_genre_books(
        db=db,
        genre_id=genre_id,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )
