from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import BorrowingHistory, BorrowingHistoryCreate
from app.crud import create_borrowing, get_borrowing_history
from app.dependencies import get_db

router = APIRouter()

# ------------------------------------
# Endpoints for Borrowing History
# ------------------------------------

@router.post("/borrow/", response_model=BorrowingHistory)
async def borrow_book_endpoint(
    borrowing: BorrowingHistoryCreate, db: Session = Depends(get_db)
) -> BorrowingHistory:
    """Borrow a book."""
    return create_borrowing(db=db, borrowing=borrowing)

@router.get("/books/{book_id}/history", response_model=list[BorrowingHistory])
async def get_borrowing_history_endpoint(
    book_id: int, db: Session = Depends(get_db)
) -> list[BorrowingHistory]:
    """Retrieve borrowing history for a specific book."""
    return get_borrowing_history(db=db, book_id=book_id)
