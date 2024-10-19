from pydantic import BaseModel, constr, condate
from typing import List, Optional
from datetime import date

# ------------------------------------
# Pydantic models for Books
# ------------------------------------

class BookBase(BaseModel):
    title: str
    isbn: str
    publish_date: date
    publisher_id: int
    author: "Author"
    genre: "Genre"

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True



# ------------------------------------
# Pydantic models for Authors
# ------------------------------------

class AuthorBase(BaseModel):
    name: str
    birthdate: condate(le=date.today())

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True

# ------------------------------------
# Pydantic models for Genres
# ------------------------------------

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True

# ------------------------------------
# Pydantic models for Publishers
# ------------------------------------

class PublisherBase(BaseModel):
    name: str
    established_year: int
    books: List[Book]

class PublisherCreate(PublisherBase):
    pass

class Publisher(PublisherBase):
    id: int

    class Config:
        orm_mode = True

# ------------------------------------
# Pydantic models for Borrowers
# ------------------------------------

class BorrowerBase(BaseModel):
    name: str

class BorrowerCreate(BorrowerBase):
    pass

class Borrower(BorrowerBase):
    id: int

    class Config:
        orm_mode = True

# ------------------------------------
# Borrowing History Schemas
# ------------------------------------

class BorrowingHistoryBase(BaseModel):
    book_id: int
    borrower_id: int
    borrow_date: date
    return_date: date | None = None

class BorrowingHistoryCreate(BorrowingHistoryBase):
    """Schema for creating a new borrowing record."""
    pass

class BorrowingHistory(BorrowingHistoryBase):
    """Schema for returning borrowing history details."""
    id: int

    class Config:
        orm_mode = True
