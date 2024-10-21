def test_register_user(client):
    user_data = {"email": "testuser@example.com", "password": "testpassword"}

    response = client.post("/register", json=user_data)

    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


def test_register_existing_user(client):
    user_data = {
        "email": "existinguser@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=user_data)

    response = client.post("/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_user(client):
    user_data = {"email": "loginuser@example.com", "password": "testpassword"}
    client.post("/register", json=user_data)

    login_data = {
        "username": "loginuser@example.com",
        "password": "testpassword",
    }
    response = client.post("/login", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_email(client):
    login_data = {
        "username": "nonexistent@example.com",
        "password": "testpassword",
    }
    response = client.post("/login", data=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_invalid_password(client):
    user_data = {"email": "loginuser2@example.com", "password": "testpassword"}
    client.post("/register", json=user_data)

    login_data = {
        "username": "loginuser2@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/login", data=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
