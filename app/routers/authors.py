from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Author, AuthorCreate
from app.crud import create_author, get_author, get_authors
from app.dependencies import get_db

router = APIRouter()

# ------------------------------------
# Endpoints for Authors
# ------------------------------------

@router.post("/authors/", response_model=Author)
async def create_author_endpoint(
    author: AuthorCreate, db: Session = Depends(get_db)
) -> Author:
    """Create a new author."""
    return create_author(db=db, author=author)

@router.get("/authors/", response_model=list[Author])
async def get_authors_endpoint(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[Author]:
    """Retrieve a list of authors with pagination."""
    return get_authors(db=db, skip=skip, limit=limit)

@router.get("/authors/{author_id}", response_model=Author)
async def get_author_endpoint(
    author_id: int, db: Session = Depends(get_db)
) -> Author:
    """Retrieve an author by their ID."""
    db_author = get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author
