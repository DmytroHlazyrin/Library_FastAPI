from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Genre, GenreCreate
from app.crud import create_genre, get_genre, get_genres
from app.dependencies import get_db

router = APIRouter()

# ------------------------------------
# Endpoints for Genres
# ------------------------------------

@router.post("/genres/", response_model=Genre)
async def create_genre_endpoint(
    genre: GenreCreate, db: Session = Depends(get_db)
) -> Genre:
    """Create a new genre."""
    return create_genre(db=db, genre=genre)

@router.get("/genres/", response_model=list[Genre])
async def get_genres_endpoint(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[Genre]:
    """Retrieve a list of genres with pagination."""
    return get_genres(db=db, skip=skip, limit=limit)

@router.get("/genres/{genre_id}", response_model=Genre)
async def get_genre_endpoint(
    genre_id: int, db: Session = Depends(get_db)
) -> Genre:
    """Retrieve a genre by its ID."""
    db_genre = get_genre(db=db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre
