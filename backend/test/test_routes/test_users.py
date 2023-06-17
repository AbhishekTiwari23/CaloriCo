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