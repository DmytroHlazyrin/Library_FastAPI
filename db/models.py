from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.engine import Base


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    birthdate = Column(Date)

    # Relationship to Book model
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    isbn = Column(String, nullable=False)  # ISBN can repeat
    publish_date = Column(Date, nullable=False)
    number_of_copies = Column(Integer, nullable=False, default=1)

    # Foreign key and relationship with Publisher
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    publisher = relationship("Publisher", back_populates="books")

    # Foreign key and relationship with Author
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    # Foreign key and relationship with Genre
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    genre = relationship("Genre", back_populates="books")

    # Relationship to BorrowingHistory model
    borrowings = relationship("BorrowingHistory", back_populates="book")


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship to Book model
    books = relationship("Book", back_populates="genre")


class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    established_year = Column(Integer, nullable=False)

    # Relationship to Book model
    books = relationship("Book", back_populates="publisher")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(
        String, unique=True, index=True, nullable=False
    )  # Unique email for each user
    hashed_password = Column(
        String, nullable=False
    )  # Hashed password for security
    is_admin = Column(
        Boolean, default=False
    )  # Indicates if the user is an admin
    max_books = Column(
        Integer, default=5
    )  # Limit on the number of books the user can borrow

    # Relationship to BorrowingHistory model
    borrowings = relationship("BorrowingHistory", back_populates="user")


class BorrowingHistory(Base):
    __tablename__ = "borrowing_history"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    # Relationship to User model
    user = relationship("User", back_populates="borrowings")

    # Relationship to Book model
    book = relationship("Book", back_populates="borrowings")
