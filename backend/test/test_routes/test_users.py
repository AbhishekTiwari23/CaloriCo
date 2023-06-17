# test to get user by username
def test_get_user_by_username(client):

    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
        "join_date": "2021-01-01",
        "role": "user",
        "expected_calories": 2000

    }
    crate_user_response = client.post("/auth/SighUp", json=user_data)
    auth_user_response = client.post("/auth/token", data={"username": "testuser", "password": "testing"})

    # Act
    response = client.get("/users/username/testuser?auth_token=" + auth_user_response.json()["access_token"])

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@nofoobar.com"

# test to get user by username with invalid token
def test_get_user_by_username_with_incorrect_credentiasls(client):

    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
        "join_date": "2021-01-01",
        "role": "user",
        "expected_calories": 2000

    }
    crate_user_response = client.post("/auth/SighUp", json=user_data)

    # Act
    response = client.get("/users/username/testuser?auth_token=" +"" + "invalid")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"

# test to get user by email
def test_get_user_by_email(client):

    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
        "join_date": "2021-01-01",
        "role": "user",
        "expected_calories": 2000

    }
    crate_user_response = client.post("/auth/SighUp", json=user_data)
    auth_user_response = client.post("/auth/token", data={"username": "testuser", "password": "testing"})

    # Act
    response = client.get("/usersEmail/testuser@nofoobar.com?auth_token=" + auth_user_response.json()["access_token"])

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@nofoobar.com"

# test to get user by email
def test_get_user_by_email_incorrect(client):

    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
        "join_date": "2021-01-01",
        "role": "user",
        "expected_calories": 2000

    }
    crate_user_response = client.post("/auth/SighUp", json=user_data)
    auth_user_response = client.post("/auth/token", data={"username": "testuser", "password": "testing"})

    # Act
    response = client.get("/usersEmail/testuser@nobar.com?auth_token=" + auth_user_response.json()["access_token"])

    assert response.status_code == 404
    assert response.json()["detail"] == "User with email testuser@nobar.com not found"
