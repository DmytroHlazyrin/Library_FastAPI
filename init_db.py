from sqlalchemy.orm import Session
from db.engine import SessionLocal
from db.models import Author, Genre, Publisher, Book
from datetime import date


# Function to create initial data
def init_db() -> None:
    """Create initial data in the database."""
    db: Session = SessionLocal()

    authors = [
        Author(name="Author One", birthdate=date(1980, 1, 1)),
        Author(name="Author Two", birthdate=date(1975, 5, 15)),
        Author(name="Author Three", birthdate=date(1990, 7, 20)),
    ]
    db.add_all(authors)
    db.commit()

    # Create genres
    genres = [
        Genre(name="Fiction"),
        Genre(name="Non-Fiction"),
        Genre(name="Science Fiction"),
    ]
    db.add_all(genres)
    db.commit()

    # Create publishers
    publishers = [
        Publisher(name="Publisher One", established_year=1990),
        Publisher(name="Publisher Two", established_year=2000),
        Publisher(name="Publisher Three", established_year=2010),
    ]
    db.add_all(publishers)
    db.commit()

    # Create books
    books = [
        Book(title="Book One", isbn="1234567890123",
             publish_date=date(2020, 1, 1),
             author_id=1, genre_id=1, publisher_id=1),
        Book(title="Book Two", isbn="1234567890124",
             publish_date=date(2021, 1, 1),
             author_id=1, genre_id=2, publisher_id=2),
        Book(title="Book Three", isbn="1234567890125",
             publish_date=date(2019, 1, 1),
             author_id=2, genre_id=1, publisher_id=1),
        Book(title="Book Four", isbn="1234567890126",
             publish_date=date(2018, 1, 1),
             author_id=2, genre_id=3, publisher_id=3),
        Book(title="Book Five", isbn="1234567890127",
             publish_date=date(2022, 1, 1),
             author_id=3, genre_id=2, publisher_id=2),
        Book(title="Book Six", isbn="1234567890128",
             publish_date=date(2017, 1, 1),
             author_id=3, genre_id=1, publisher_id=1),
        Book(title="Book Seven", isbn="1234567890129",
             publish_date=date(2023, 1, 1),
             author_id=1, genre_id=3, publisher_id=3),
        Book(title="Book Eight", isbn="1234567890130",
             publish_date=date(2021, 5, 1),
             author_id=2, genre_id=2, publisher_id=2),
        Book(title="Book Nine", isbn="1234567890131",
             publish_date=date(2024, 1, 1),
             author_id=3, genre_id=1, publisher_id=1),
        Book(title="Book Ten", isbn="1234567890132",
             publish_date=date(2025, 1, 1),
             author_id=1, genre_id=3, publisher_id=3),
    ]
    db.add_all(books)
    db.commit()


if __name__ == "__main__":
    init_db()
