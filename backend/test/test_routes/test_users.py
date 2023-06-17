import json

def test_create_user(client):
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

    # Act
    response = client.post("/auth/SighUp", json=user_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["password"] != "testing"
    assert response.json()["join_date"] == "2021-01-01"
    assert response.json()["role"] == "user"
    assert response.json()["expected_calories"] == 2000

