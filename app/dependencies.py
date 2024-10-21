from app.jwt_handler import verify_token
from db.engine import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import crud
from db import models

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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Fetch the current user based on the JWT token."""
    credentials_exception = HTTPException(
        status_code=403, detail="Could not validate credentials"
    )
    email = verify_token(token, credentials_exception)
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


def admin_required(current_user: models.User = Depends(get_current_user)):
    """Ensure the current user is an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Operation not permitted. Admins only."
        )
