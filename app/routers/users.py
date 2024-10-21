from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import BorrowingHistory, User, BookBase
from app.crud import (
    get_user_borrowing_history,
    get_active_borrowing_book,
    get_users,
    get_debtors,
)
from app.dependencies import get_db, admin_required, get_current_user
from db import models
from db.models import Book

router = APIRouter()


# ------------------------------------
# Endpoints for Borrowings
# ------------------------------------
@router.get("/me/history", response_model=list[BorrowingHistory])
async def get_borrowing_history_endpoint(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> list[BorrowingHistory]:
    """Retrieve borrowing history for current user."""
    return get_user_borrowing_history(db=db, user_id=current_user.id)


@router.get("/me/debts", response_model=list[BookBase])
async def get_current_user_active_borrowings_endpoint(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> list[Book]:
    """Retrieve active borrowing books for current user."""
    return get_active_borrowing_book(db=db, user_id=current_user.id)


@router.get("/users", response_model=list[User])
async def get_users_endpoint(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
    sort_by: str = "email",
    sort_order: str = "asc",
    current_user: models.User = Depends(admin_required),
) -> list[User]:
    """Retrieve a list of users."""
    return get_users(
        db=db,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/users/{user_id}/debts", response_model=list[BookBase])
async def get_user_active_borrowings_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(admin_required),
) -> list[Book]:
    """Retrieve active borrowing books for current user."""
    return get_active_borrowing_book(db=db, user_id=user_id)


@router.get("/users/{user_id}/history", response_model=list[BorrowingHistory])
async def get_user_borrowing_history_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(admin_required),
) -> list[BorrowingHistory]:
    """Retrieve borrowing history for a specific book."""
    return get_user_borrowing_history(db=db, user_id=user_id)


@router.get("/debtors", response_model=list[User])
async def get_debtors_endpoint(
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    sort_by: str = None,
    sort_order: str = None,
    current_user: models.User = Depends(admin_required),
) -> list[User]:
    """Retrieve a list of debtors."""
    return get_debtors(
        db=db,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )
