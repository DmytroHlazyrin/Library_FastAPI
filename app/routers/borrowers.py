from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Borrower, BorrowerCreate
from app.crud import create_borrower, get_borrower, get_borrowers
from app.dependencies import get_db

router = APIRouter()

# ------------------------------------
# Endpoints for Borrowers
# ------------------------------------

@router.post("/borrowers/", response_model=Borrower)
async def create_borrower_endpoint(
    borrower: BorrowerCreate, db: Session = Depends(get_db)
) -> Borrower:
    """Create a new borrower."""
    return create_borrower(db=db, borrower=borrower)

@router.get("/borrowers/", response_model=list[Borrower])
async def get_borrowers_endpoint(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[Borrower]:
    """Retrieve a list of borrowers with pagination."""
    return get_borrowers(db=db, skip=skip, limit=limit)

@router.get("/borrowers/{borrower_id}", response_model=Borrower)
async def get_borrower_endpoint(
    borrower_id: int, db: Session = Depends(get_db)
) -> Borrower:
    """Retrieve a borrower by their ID."""
    db_borrower = get_borrower(db=db, borrower_id=borrower_id)
    if db_borrower is None:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return db_borrower
