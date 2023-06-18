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

# test to delete a user
def test_delete_user(client):
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

    response = client.delete("/usersEmail/testuser@nofoobar.com?auth_token=" + auth_user_response.json()["access_token"])

    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted successfully"

# test to delete a user with invalid token
def test_delete_user_with_invalid_token(client):
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

    response = client.delete("/usersEmail/testur@nofoobar.com?auth_token=" + auth_user_response.json()["access_token"])

    assert response.status_code == 404
    assert response.json()["detail"] == "User with email testur@nofoobar.com not found"

#  test to update a user by email with invalid email
def test_update_user_by_email_invalid(client):
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
    assert crate_user_response.status_code == 200
    auth_user_response = client.post("/auth/token", data={"username": "testuser", "password": "testing"})
    assert auth_user_response.status_code == 200
    access_token = auth_user_response.json()["access_token"]

    updated_user_data = {
        "first_name": "Updated John",
        "last_name": "Updated Doe",
        "username": "updated_testuser",
        "email": "updated_testuser@nofoobar.com",
        "password": "updated_testing",
        "join_date": "2021-01-01",
        "role": "admin",
        "expected_calories": 2500
    }
    # Act
    response = client.put(
        f"/users/update/testuser@nofbar.com?auth_token={access_token}",
        json=updated_user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "User with email testuser@nofbar.com not found"

#  test to update a user by email
def test_update_user_by_email(client):
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
    assert crate_user_response.status_code == 200
    auth_user_response = client.post("/auth/token", data={"username": "testuser", "password": "testing"})
    assert auth_user_response.status_code == 200
    access_token = auth_user_response.json()["access_token"]

    updated_user_data = {
        "first_name": "Updated John",
        "last_name": "Updated Doe",
        "username": "updated_testuser",
        "email": "updated_testuser@nofoobar.com",
        "password": "updated_testing",
        "join_date": "2021-01-01",
        "role": "admin",
        "expected_calories": 2500
    }
    # Act
    response = client.put(
        f"/users/update/testuser@nofoobar.com?auth_token={access_token}",
        json=updated_user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated John"
    assert response.json()["last_name"] == "Updated Doe"
    assert response.json()["username"] == "updated_testuser"
    assert response.json()["email"] == "updated_testuser@nofoobar.com"
    assert response.json()["role"] == "admin"
    assert response.json()["expected_calories"] == 2500




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



