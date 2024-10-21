from tests.conftest import NUM_OF_ITEMS


def test_get_books(client, admin_user, create_books):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/books", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == NUM_OF_ITEMS


def test_get_books_with_sorting(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/books?sort_by=title&sort_order=asc&limit=5&offset=0",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5

    book_titles = [book["title"] for book in response.json()]
    assert book_titles == sorted(book_titles)


def test_get_books_with_limit_offset(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/books?limit=3&offset=2", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

    expected_books = [f"Book {i}" for i in range(2, 5)]
    book_titles = [book["title"] for book in response.json()]
    assert book_titles == expected_books


def test_create_book_as_admin(client, admin_user):
    book_data = {
        "title": "Test Book",
        "isbn": "9781501161247",
        "publish_date": "2022-01-01",
        "number_of_copies": 10,
        "author_id": 1,
        "publisher_id": 1,
        "genre_id": 1,
    }

    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.post(
        "/books", json=book_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
