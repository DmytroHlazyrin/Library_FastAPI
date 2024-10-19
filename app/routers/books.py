from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Book, BookCreate
from app.crud import create_book, get_book, get_books
from app.dependencies import get_db

router = APIRouter()

# ------------------------------------
# Endpoints for Books
# ------------------------------------

@router.post("/books/", response_model=Book)
async def create_book_endpoint(
    book: BookCreate, db: Session = Depends(get_db)
) -> Book:
    """Create a new book."""
    return create_book(db=db, book=book)

@router.get("/books/", response_model=list[Book])
async def get_books_endpoint(
    offset: int = 0,
    limit: int = 10,
    sort_by: str = None,
    sort_order: str = "asc",
    db: Session = Depends(get_db)
) -> list[Book]:
    """Retrieve a list of books with pagination."""
    return get_books(db=db, offset=offset, limit=limit, sort_by=sort_by, sort_order=sort_order)

@router.get("/books/{book_id}", response_model=Book)
async def get_book_endpoint(
    book_id: int, db: Session = Depends(get_db)
) -> Book:
    """Retrieve a book by its ID."""
    db_book = get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
