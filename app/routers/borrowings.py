from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import BorrowingHistory, BorrowingHistoryCreate
from app.crud import get_borrowing_history, borrow_book, return_book
from app.dependencies import get_db, admin_required, get_current_user
from db import models

router = APIRouter()


# ------------------------------------
# Endpoints for Borrowings
# ------------------------------------
@router.post("/books/{book_id}/borrow", response_model=BorrowingHistoryCreate)
async def borrow_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> BorrowingHistory:
    """Borrow a book."""
    return borrow_book(db=db, book_id=book_id, user_id=current_user.id)


@router.post("/books/{book_id}/return", response_model=BorrowingHistoryCreate)
async def return_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> BorrowingHistory:
    """Borrow a book."""
    return return_book(db=db, book_id=book_id, user_id=current_user.id)


@router.get("/books/{book_id}/history", response_model=list[BorrowingHistory])
async def get_borrowing_history_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(admin_required),
) -> list[BorrowingHistory]:
    """Retrieve borrowing history for a specific book."""
    return get_borrowing_history(db=db, book_id=book_id)
