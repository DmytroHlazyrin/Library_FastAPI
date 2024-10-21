def test_borrow_book(client, user, create_books):
    response = client.post(
        "/login", data={"username": user.email, "password": "userpassword"}
    )
    token = response.json().get("access_token")

    response = client.post(
        "/books/1/borrow", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["book_id"] == 1


def test_return_book(client, user):
    response = client.post(
        "/login", data={"username": user.email, "password": "userpassword"}
    )
    token = response.json().get("access_token")

    client.post(
        "/books/1/borrow", headers={"Authorization": f"Bearer {token}"}
    )

    response = client.post(
        "/books/1/return", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["book_id"] == 1


def test_get_borrowing_history_as_admin(client, admin_user):
    response = client.post(
        "/login",
        data={"username": admin_user.email, "password": "adminpassword"},
    )
    token = response.json().get("access_token")

    client.post(
        "/books/1/borrow", headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        "/books/1/history", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_borrowing_history_as_non_admin(client, user):
    response = client.post(
        "/login", data={"username": user.email, "password": "userpassword"}
    )
    token = response.json().get("access_token")

    response = client.get(
        "/books/1/history", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
