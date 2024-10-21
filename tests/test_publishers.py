from tests.conftest import NUM_OF_ITEMS


def test_create_publisher_as_admin(client, admin_user):
    publisher_data = {
        "name": "Test Publisher",
        "established_year": 2020,
    }
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.post(
        "/publishers",
        json=publisher_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == publisher_data["name"]


def test_get_publishers(client, admin_user, create_publishers):

    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/publishers", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == NUM_OF_ITEMS


def test_get_publishers_with_sorting(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/publishers?sort_by=name&sort_order=asc&limit=5&offset=0",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5

    publisher_names = [publisher["name"] for publisher in response.json()]
    assert publisher_names == sorted(publisher_names)


def test_get_publishers_with_limit_offset(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    response = client.get(
        "/publishers?limit=3&offset=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

    expected_publishers = [f"Publisher {i}" for i in range(2, 5)]
    publisher_names = [publisher["name"] for publisher in response.json()]
    assert publisher_names == expected_publishers
