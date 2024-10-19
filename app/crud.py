from typing import Optional

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

import db.models as models
from app import schemas


# ------------------------------------
# CRUD operations for Books
# ------------------------------------

def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """Create a new book."""
    # Ensure authors exist
    authors = db.query(models.Author).filter(models.Author.id.in_(book.author_ids)).all()
    if len(authors) != len(book.author_ids):
        raise ValueError("Some authors not found")

    # Ensure genres exist
    genres = db.query(models.Genre).filter(models.Genre.id.in_(book.genre_ids)).all()
    if len(genres) != len(book.genre_ids):
        raise ValueError("Some genres not found")

    db_book = models.Book(**book.dict())
    db_book.authors = authors
    db_book.genres = genres
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
    sort_order: str = "asc"
) -> list[models.Book]:
    """Retrieve a list of books with optional sorting."""
    query = db.query(models.Book)

    # Add sorting logic
    if sort_by:
        if sort_by == "title":
            query = query.order_by(asc(models.Book.title) if sort_order == "asc" else desc(models.Book.title))
        elif sort_by == "publish_date":
            query = query.order_by(asc(models.Book.publish_date) if sort_order == "asc" else desc(models.Book.publish_date))
        elif sort_by == "author":
            query = query.join(models.Book.author).order_by(asc(models.Author.name) if sort_order == "asc" else desc(models.Author.name))

    return query.offset(offset).limit(limit).all()


# ------------------------------------
# CRUD operations for Authors
# ------------------------------------

def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """Create a new author in the database."""
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int) -> models.Author:
    """Retrieve an author by their ID."""
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db: Session, offset: int = 0, limit: int = 10) -> list[models.Author]:
    """Retrieve a list of authors with pagination."""
    return db.query(models.Author).offset(offset).limit(limit).all()


# ------------------------------------
# CRUD operations for Genres
# ------------------------------------

def create_genre(db: Session, genre: schemas.GenreCreate) -> models.Genre:
    """Create a new genre in the database."""
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_genre(db: Session, genre_id: int) -> models.Genre:
    """Retrieve a genre by its ID."""
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()

def get_genres(db: Session, offset: int = 0, limit: int = 10) -> list[models.Genre]:
    """Retrieve a list of genres with pagination."""
    return db.query(models.Genre).offset(offset).limit(limit).all()


# ------------------------------------
# CRUD operations for Publishers
# ------------------------------------

def create_publisher(db: Session, publisher: schemas.PublisherCreate) -> models.Publisher:
    """Create a new publisher in the database."""
    db_publisher = models.Publisher(**publisher.dict())
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher

def get_publisher(db: Session, publisher_id: int) -> models.Publisher:
    """Retrieve a publisher by their ID."""
    return db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()

def get_publishers(db: Session, offset: int = 0, limit: int = 10) -> list[models.Publisher]:
    """Retrieve a list of publishers with pagination."""
    return db.query(models.Publisher).offset(offset).limit(limit).all()


# ------------------------------------
# CRUD operations for Borrowers
# ------------------------------------

def create_borrower(db: Session, borrower: schemas.BorrowerCreate) -> models.Borrower:
    """Create a new borrower in the database."""
    db_borrower = models.Borrower(**borrower.dict())
    db.add(db_borrower)
    db.commit()
    db.refresh(db_borrower)
    return db_borrower

def get_borrower(db: Session, borrower_id: int) -> models.Borrower:
    """Retrieve a borrower by their ID."""
    return db.query(models.Borrower).filter(models.Borrower.id == borrower_id).first()

def get_borrowers(db: Session, offset: int = 0, limit: int = 10) -> list[models.Borrower]:
    """Retrieve a list of borrowers with pagination."""
    return db.query(models.Borrower).offset(offset).limit(limit).all()


# ------------------------------------
# Create Borrowing
# ------------------------------------

def create_borrowing(db: Session, borrowing: schemas.BorrowingHistoryCreate) -> models.BorrowingHistory:
    """Create a new borrowing record."""
    # Ensure the book is available for borrowing
    book = db.query(models.Book).filter(models.Book.id == borrowing.book_id).first()
    if not book:
        raise ValueError("Book not found")

    # Ensure the borrower exists
    borrower = db.query(models.Borrower).filter(models.Borrower.id == borrowing.borrower_id).first()
    if not borrower:
        raise ValueError("Borrower not found")

    # Create the borrowing history record
    db_borrowing = models.BorrowingHistory(**borrowing.dict())
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


# ------------------------------------
# Get Borrowing History
# ------------------------------------

def get_borrowing_history(db: Session, book_id: int) -> list[models.BorrowingHistory]:
    """Retrieve the borrowing history for a specific book."""
    return db.query(models.BorrowingHistory).filter(models.BorrowingHistory.book_id == book_id).all()
