from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.engine import SessionLocal

# ------------------------------------
# Dependency to get DB session
# ------------------------------------

def get_db() -> Session:
    """Create a new database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------
# Custom exceptions for error handling
# ------------------------------------

class NotFoundException(HTTPException):
    """Custom exception for not found errors."""
    def __init__(self, entity: str, id: int):
        detail = f"{entity} with ID {id} not found."
        super().__init__(status_code=404, detail=detail)
