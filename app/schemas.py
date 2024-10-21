from pydantic import BaseModel, condate, field_validator, EmailStr
from pydantic_extra_types.isbn import ISBN
from datetime import date


# ------------------------------------
# Pydantic models for Users
# ------------------------------------


class UserCreate(BaseModel):
    email: EmailStr  # Validates that the email is in the correct format
    password: str  # User's password


class User(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True


# ------------------------------------
# Pydantic models for Books
# ------------------------------------


class BookBase(BaseModel):
    title: str
    isbn: ISBN
    publish_date: condate(le=date.today())
    publisher_id: int


class BookCreate(BookBase):
    author_id: int
    genre_id: int
    number_of_copies: int = 1


class Book(BookBase):
    id: int
    author: "Author"
    genre: "Genre"

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

    @field_validator("established_year")
    @classmethod
    def ensure_established_year_in_the_past(cls, value: int):
        """Validate that the established year is not in the future."""
        current_year = date.today().year
        if value > current_year:
            raise ValueError(
                f"Established year cannot be in the future "
                f"(current year: {current_year})"
            )
        return value


class PublisherCreate(PublisherBase):
    pass


class Publisher(PublisherBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------------------
# Borrowing History Schemas
# ------------------------------------


class BorrowingHistoryBase(BaseModel):
    book_id: int
    user: "User"
    borrow_date: condate(le=date.today())
    return_date: condate(le=date.today()) | None = None


class BorrowingHistoryCreate(BorrowingHistoryBase):
    """Schema for creating a new borrowing record."""

    pass


class BorrowingHistory(BorrowingHistoryBase):
    """Schema for returning borrowing history details."""

    id: int

    class Config:
        orm_mode = True
