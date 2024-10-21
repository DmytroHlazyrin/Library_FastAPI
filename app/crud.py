from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from db import models
from app import schemas
from app.security import hash_password


# ------------------------------------
# CRUD operations for Books
# ------------------------------------


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """Create a new book with appropriate validations and return it."""
    # Ensure the author exists
    author = (
        db.query(models.Author)
        .filter(models.Author.id == book.author_id)
        .first()
    )
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    # Ensure the genre exists
    genre = (
        db.query(models.Genre).filter(models.Genre.id == book.genre_id).first()
    )
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    # Ensure the publisher exists
    publisher = (
        db.query(models.Publisher)
        .filter(models.Publisher.id == book.publisher_id)
        .first()
    )
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    # Ensure the number of copies is a positive integer
    if (
        book.number_of_copies is None
        or not isinstance(book.number_of_copies, int)
        or book.number_of_copies < 0
    ):
        raise HTTPException(
            status_code=400,
            detail="Number of copies must be a positive integer",
        )

    # Ensure the publication year is a valid year
    if not date(1500, 1, 1) <= book.publish_date <= date.today():
        raise HTTPException(
            status_code=400, detail="Publication year must be realistic"
        )

    # Create and save the book in the database
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> models.Book:
    """Retrieve a book by its ID."""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(
    db: Session,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> list[models.Book]:
    """Retrieve a list of books with optional sorting."""
    query = db.query(models.Book)

    # Add sorting logic
    if sort_by:
        if sort_by == "title":
            query = query.order_by(
                asc(models.Book.title)
                if sort_order == "asc"
                else desc(models.Book.title)
            )
        elif sort_by == "publish_date":
            query = query.order_by(
                asc(models.Book.publish_date)
                if sort_order == "asc"
                else desc(models.Book.publish_date)
            )
        elif sort_by == "author":
            query = query.join(models.Book.author).order_by(
                asc(models.Author.name)
                if sort_order == "asc"
                else desc(models.Author.name)
            )

    return query.offset(offset).limit(limit).all()


# ------------------------------------
# CRUD operations for Authors
# ------------------------------------


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """Create a new author in the database."""
    # Ensure that the author's name is unique'
    if (
        db.query(models.Author)
        .filter(models.Author.name == author.name)
        .first()
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Author name must be unique. "
            f"There is already an author with name '{author.name}'.",
        )

    # Ensure the author's birthdate is a valid date'
    if author.birthdate >= date.today():
        raise HTTPException(
            status_code=400, detail="Birthdate must be a valid date."
        )

    # Create and save the author in the database
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int) -> models.Author:
    """Retrieve an author by their ID."""
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def get_authors(
    db: Session,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> list[models.Author]:
    """Retrieve a list of authors with pagination."""
    query = db.query(models.Author)
    if sort_by:
        if sort_by == "name":
            query = query.order_by(
                asc(models.Author.name)
                if sort_order == "asc"
                else desc(models.Author.name)
            )
        elif sort_by == "birthdate":
            query = query.order_by(
                asc(models.Author.birthdate)
                if sort_order == "asc"
                else desc(models.Author.birthdate)
            )

    return query.offset(offset).limit(limit).all()


def get_author_books(
    db: Session,
    author_id: int,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> list[models.Book]:
    """Retrieve a list of books by an author."""
    query = db.query(models.Book).filter(models.Book.author_id == author_id)

    if sort_by:
        if sort_by == "title":
            query = query.order_by(
                asc(models.Book.title)
                if sort_order == "asc"
                else desc(models.Book.title)
            )
        elif sort_by == "publish_date":
            query = query.order_by(
                asc(models.Book.publish_date)
                if sort_order == "asc"
                else desc(models.Book.publish_date)
            )

    return query.offset(offset).limit(limit).all()


# ------------------------------------
# CRUD operations for Genres
# ------------------------------------


def create_genre(db: Session, genre: schemas.GenreCreate) -> models.Genre:
    """Create a new genre in the database."""
    # Ensure that the genre's name is unique'
    if db.query(models.Genre).filter(models.Genre.name == genre.name).first():
        raise HTTPException(
            status_code=400,
            detail=f"Genre name must be unique. "
            f"There is already a genre with name '{genre.name}'.",
        )

    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def get_genre(db: Session, genre_id: int) -> models.Genre:
    """Retrieve a genre by its ID."""
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


def get_genres(
    db: Session,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> list[models.Genre]:
    """Retrieve a list of genres with pagination."""
    query = db.query(models.Genre)
    if sort_by:
        if sort_by == "name":
            query = query.order_by(
                asc(models.Genre.name)
                if sort_order == "asc"
                else desc(models.Genre.name)
            )

    return query.offset(offset).limit(limit).all()


def get_genre_books(
    db: Session,
    genre_id: int,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> list[models.Book]:
    """Retrieve a list of books by a genre."""
    query = db.query(models.Book).filter(models.Book.genre_id == genre_id)

    if sort_by:
        if sort_by == "title":
            query = query.order_by(
                asc(models.Book.title)
                if sort_order == "asc"
                else desc(models.Book.title)
            )
        elif sort_by == "publish_date":
            query = query.order_by(
                asc(models.Book.publish_date)
                if sort_order == "asc"
                else desc(models.Book.publish_date)
            )
        elif sort_by == "author":
            query = query.join(models.Book.author).order_by(
                asc(models.Author.name)
                if sort_order == "asc"
                else desc(models.Author.name)
            )

    return query.offset(offset).limit(limit).all()


# ------------------------------------
# CRUD operations for Publishers
# ------------------------------------


def create_publisher(
    db: Session, publisher: schemas.PublisherCreate
) -> models.Publisher:
    """Create a new publisher in the database."""
    # Ensure that the genre's name is unique'
    if (
        db.query(models.Publisher)
        .filter(models.Publisher.name == publisher.name)
        .first()
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Publisher name must be unique. "
            f"There is already a publisher with name '{publisher.name}'.",
        )

    db_publisher = models.Publisher(**publisher.dict())
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


def get_publisher(db: Session, publisher_id: int) -> models.Publisher:
    """Retrieve a publisher by their ID."""
    return (
        db.query(models.Publisher)
        .filter(models.Publisher.id == publisher_id)
        .first()
    )


def get_publishers(
    db: Session,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> list[models.Publisher]:
    """Retrieve a list of genres with pagination."""
    query = db.query(models.Publisher)
    if sort_by:
        if sort_by == "name":
            query = query.order_by(
                asc(models.Publisher.name)
                if sort_order == "asc"
                else desc(models.Publisher.name)
            )
        elif sort_by == "established_year":
            query = query.order_by(
                asc(models.Publisher.established_year)
                if sort_order == "asc"
                else desc(models.Publisher.established_year)
            )

    return query.offset(offset).limit(limit).all()


# ------------------------------------
# CRUD operations for Users
# ------------------------------------


def create_user(db: Session, user_data: schemas.UserCreate) -> models.User:
    """Creates a new user with a hashed password."""
    hashed_password = hash_password(user_data.password)
    db_user = models.User(
        email=user_data.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    """Returns a user by email if they exist."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> list[models.User]:
    """Returns a list of users with pagination."""
    query = db.query(models.User)
    if sort_by:
        if sort_by == "email":
            query = query.order_by(
                asc(models.User.email)
                if sort_order == "asc"
                else desc(models.User.email)
            )

    return query.offset(offset).limit(limit).all()


def get_debtors(
    db: Session,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> list[models.User]:
    """Returns a list of users who have active borrowings."""
    query = (
        db.query(models.User)
        .join(
            models.BorrowingHistory,
            models.User.id == models.BorrowingHistory.user_id,
        )
        .filter(models.BorrowingHistory.return_date.is_(None))
    )

    if sort_by:
        if sort_by == "email":
            query = query.order_by(
                asc(models.User.email)
                if sort_order == "asc"
                else desc(models.User.email)
            )

    return query.offset(offset).limit(limit).all()


# ------------------------------------
# Borrowing
# ------------------------------------
def get_available_books_count(db: Session, book_id: int) -> int:
    """Returns the count of available copies of a specific book."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    total_copies = book.number_of_copies
    borrowed_count = (
        db.query(models.BorrowingHistory)
        .filter(
            models.BorrowingHistory.book_id == book_id,
            models.BorrowingHistory.return_date.is_(None),
        )
        .count()
    )

    return total_copies - borrowed_count


def borrow_book(
    db: Session, user_id: int, book_id: int
) -> models.BorrowingHistory:
    """Allows a user to borrow a book if they are
    within their limit and the book is available."""
    # Check user's current borrowings
    user = db.query(models.User).filter(models.User.id == user_id).first()
    current_borrowings = (
        db.query(models.BorrowingHistory)
        .filter(
            models.BorrowingHistory.user_id == user_id,
            models.BorrowingHistory.return_date.is_(None),
        )
        .count()
    )

    if current_borrowings >= user.max_books:
        raise HTTPException(status_code=400, detail="Borrowing limit exceeded")

    # Check if the book is available
    available_copies = get_available_books_count(db, book_id)
    if available_copies == 0:
        raise HTTPException(status_code=400, detail="No available copies")

    # Borrow the book
    borrowing = models.BorrowingHistory(
        user_id=user_id, book_id=book_id, borrow_date=date.today()
    )
    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)

    return borrowing


def return_book(
    db: Session, user_id: int, book_id: int
) -> models.BorrowingHistory:
    """Allows a user to return a borrowed book."""
    borrowing = (
        db.query(models.BorrowingHistory)
        .filter(
            models.BorrowingHistory.user_id == user_id,
            models.BorrowingHistory.book_id == book_id,
            models.BorrowingHistory.return_date.is_(None),
        )
        .first()
    )

    if borrowing is None:
        raise HTTPException(
            status_code=404,
            detail="No active borrowing found for this book and user",
        )

    borrowing.return_date = date.today()
    db.commit()
    db.refresh(borrowing)

    return borrowing


# ------------------------------------
# Get Borrowing History
# ------------------------------------


def get_borrowing_history(
    db: Session, book_id: int
) -> list[models.BorrowingHistory]:
    """Retrieve the borrowing history for a specific book."""
    return (
        db.query(models.BorrowingHistory)
        .filter(models.BorrowingHistory.book_id == book_id)
        .all()
    )


def get_user_borrowing_history(
    db: Session, user_id: int
) -> list[models.BorrowingHistory]:
    """Retrieve the borrowing history for a specific user."""
    return (
        db.query(models.BorrowingHistory)
        .filter(models.BorrowingHistory.user_id == user_id)
        .all()
    )


def get_active_borrowing_book(db: Session, user_id) -> list[models.Book]:
    """Retrieve the currently borrowed book for a specific user."""
    return (
        db.query(models.Book)
        .join(
            models.BorrowingHistory,
            models.Book.id == models.BorrowingHistory.book_id,
        )
        .filter(
            models.BorrowingHistory.user_id == user_id,
            models.BorrowingHistory.return_date.is_(None),
        )
        .all()
    )
