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

# test to get all users
def test_get_all_users(client):
    # Arrange
    user_data1 = {
        "first_name": "John1",
        "last_name": "Doe1",
        "username": "testuser1",
        "email": "testuser@nofoobar1.com",
        "password": "testing1",
        "join_date": "2021-01-01",
        "role": "admin",
        "expected_calories": 2000
    }
    crate_user_response1 = client.post("/auth/SighUp", json=user_data1)

    user_data2 = {
        "first_name": "John2",
        "last_name": "Doe2",
        "username": "testuser2",
        "email": "testuser@nofoobar2.com",
        "password": "testing2",
        "join_date": "2021-01-01",
        "role": "user",
        "expected_calories": 2000
    }
    crate_user_response2 = client.post("/auth/SighUp", json=user_data2)

    user_data3 = {
        "first_name": "John3",
        "last_name": "Doe3",
        "username": "testuser3",
        "email": "testuser@nofoobar3.com",
        "password": "testing3",
        "join_date": "2021-01-01",
        "role": "user",
        "expected_calories": 2000
    }
    crate_user_response3 = client.post("/auth/SighUp", json=user_data3)

    auth_user_response = client.post("/auth/token", data={"username": "testuser1", "password": "testing1"})

    # Act
    access_token = auth_user_response.json()["access_token"]
    response = client.get(f"/users/user/all?auth_token={access_token}&page=1&size=100")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2 # 2 users created


# test to get all users with invalid token
def test_get_all_users_neg(client):
    # Arrange
    user_data1 = {
        "first_name": "John1",
        "last_name": "Doe1",
        "username": "testuser1",
        "email": "testuser@nofoobar1.com",
        "password": "testing1",
        "join_date": "2021-01-01",
        "role": "admin",
        "expected_calories": 2000
    }
    crate_user_response1 = client.post("/auth/SighUp", json=user_data1)

    user_data2 = {
        "first_name": "John2",
        "last_name": "Doe2",
        "username": "testuser2",
        "email": "testuser@nofoobar2.com",
        "password": "testing2",
        "join_date": "2021-01-01",
        "role": "user",
        "expected_calories": 2000
    }
    crate_user_response2 = client.post("/auth/SighUp", json=user_data2)

    user_data3 = {
        "first_name": "John3",
        "last_name": "Doe3",
        "username": "testuser3",
        "email": "testuser@nofoobar3.com",
        "password": "testing3",
        "join_date": "2021-01-01",
        "role": "user",
        "expected_calories": 2000
    }
    crate_user_response3 = client.post("/auth/SighUp", json=user_data3)

    auth_user_response = client.post("/auth/token", data={"username": "test", "password": "testing1"})

    # Act
    assert auth_user_response.status_code == 401
    assert auth_user_response.json()["detail"] == "Incorrect username or password"

    # Assert


