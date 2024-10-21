from tests.conftest import NUM_OF_ITEMS


def test_create_genre_as_admin(client, admin_user, create_genres):
    genre_data = {
        "name": "Test Genre",
    }
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.post(
        "/genres",
        json=genre_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == genre_data["name"]


def test_get_genres(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/genres", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == NUM_OF_ITEMS


def test_get_genres_with_sorting(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/genres?sort_by=name&sort_order=asc&limit=5&offset=0",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5

    genre_names = [genre["name"] for genre in response.json()]
    assert genre_names == sorted(genre_names)


def test_get_genres_with_limit_offset(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/genres?limit=3&offset=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

    expected_genres = [f"Genre {i}" for i in range(2, 5)]
    genre_names = [genre["name"] for genre in response.json()]
    assert genre_names == expected_genres
