from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.engine import Base
from typing import List


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    birthdate = Column(Date)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    isbn = Column(String, nullable=False)  # ISBN can repeat
    publish_date = Column(Date, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"))

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    genre = relationship("Genre", back_populates="books")

    publisher = relationship("Publisher", back_populates="books")
    borrowings = relationship("BorrowingHistory", back_populates="book")


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    books = relationship("Book", back_populates="genre")


class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    established_year = Column(Integer, nullable=False)

    books = relationship("Book", back_populates="publisher")


class Borrower(Base):
    __tablename__ = "borrowers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    borrowings = relationship("BorrowingHistory", back_populates="borrower")

    def get_active_books(self) -> List[int]:
        """Returns a list of book IDs that have not been returned."""
        return [borrowing.book_id for borrowing in self.borrowings
                if borrowing.return_date is None]


class BorrowingHistory(Base):
    __tablename__ = "borrowing_history"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    borrower = relationship("Borrower", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
