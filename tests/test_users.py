def test_get_active_borrowings(client, user):
    response = client.post(
        "/login", data={"username": user.email, "password": "userpassword"}
    )
    assert response.status_code == 200
    token = response.json().get("access_token")

    response = client.get(
        "/me/debts", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_users_as_admin(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    assert response.status_code == 200
    token = response.json().get("access_token")

    response = client.get(
        "/users", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_active_borrowings_as_admin(client, admin_user, user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    assert response.status_code == 200
    token = response.json().get("access_token")

    response = client.get(
        f"/users/{user.id}/debts", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
