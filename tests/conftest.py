import uuid
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.dependencies import get_db
from app.main import app
from app.security import hash_password
from db import models
from db.engine import Base

DATABASE_URL = "sqlite:///./test.db"
NUM_OF_ITEMS = 10


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db):
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def admin_user(test_db):
    user_data = {
        "email": f"admin_{uuid.uuid4()}@example.com",
        "hashed_password": hash_password("adminpassword"),
        "is_admin": True,
    }
    user = models.User(**user_data)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture()
def user(test_db):
    user_data = {
        "email": f"user_{uuid.uuid4()}@example.com",
        "hashed_password": hash_password("userpassword"),
    }
    user = models.User(**user_data)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture()
def create_publishers(test_db):
    publishers = []
    for i in range(NUM_OF_ITEMS):
        publisher_data = {
            "name": f"Publisher {i}",
            "established_year": 1900 + i,
        }
        publisher = models.Publisher(**publisher_data)
        test_db.add(publisher)
        publishers.append(publisher)
    test_db.commit()
    return publishers


@pytest.fixture()
def create_genres(test_db):
    genres = []
    for i in range(NUM_OF_ITEMS):
        genre_data = {
            "name": f"Genre {i}",
        }
        genre = models.Genre(**genre_data)
        test_db.add(genre)
        genres.append(genre)
    test_db.commit()
    return genres


@pytest.fixture()
def create_authors(test_db):
    authors = []
    for i in range(NUM_OF_ITEMS):
        author_data = {
            "name": f"Author {i}",
            "birthdate": date(2000 + i, 1, 1),
        }
        author = models.Author(**author_data)
        test_db.add(author)
        authors.append(author)
    test_db.commit()
    return authors


isbn_list = [
    "9783161484100",
    "9780306406157",
    "9781402894626",
    "9780743273565",
    "9780452284234",
    "9781566199094",
    "9780198526636",
    "9780307476463",
    "9780452290488",
    "9780545139700",
    "9781594203488",
    "9780747593715",
    "9780143039433",
    "9780452284231",
    "9781501161247",
]


@pytest.fixture()
def create_books(test_db, create_authors, create_publishers, create_genres):
    books = []
    for i in range(NUM_OF_ITEMS):
        book_data = {
            "title": f"Book {i}",
            "isbn": isbn_list[i],
            "publish_date": date(2000 + i, 1, 1),
            "number_of_copies": 5,
            "author_id": create_authors[i % len(create_authors)].id,
            "publisher_id": create_publishers[i % len(create_publishers)].id,
            "genre_id": create_genres[i % len(create_genres)].id,
        }
        book = models.Book(**book_data)
        test_db.add(book)
        books.append(book)
    test_db.commit()
    return books
