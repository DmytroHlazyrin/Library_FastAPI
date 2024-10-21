from tests.conftest import NUM_OF_ITEMS


def test_create_author_as_admin(client, admin_user):
    author_data = {
        "name": f"Test Author",
        "birthdate": "1950-01-01",
    }

    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.post(
        "/authors",
        json=author_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == author_data["name"]


def test_get_authors(client, admin_user, create_authors):

    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/authors", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == NUM_OF_ITEMS


def test_get_authors_with_sorting(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/authors?sort_by=name&sort_order=asc&limit=5&offset=0",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5

    author_names = [author["name"] for author in response.json()]
    assert author_names == sorted(author_names)


def test_get_authors_with_limit_offset(client, admin_user):

    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/authors?limit=3&offset=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

    expected_authors = [f"Author {i}" for i in range(2, 5)]
    author_names = [author["name"] for author in response.json()]
    assert author_names == expected_authors
