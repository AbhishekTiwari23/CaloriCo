# test to create a new food
def test_create_new_food(client):
    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
        "join_date": "2021-01-01",
        "role": "admin",
        "expected_calories": 2000
    }

    create_user_response = client.post("/auth/SighUp", json=user_data)
    assert create_user_response.status_code == 200
    auth_user_response = client.post("/auth/token", data={"username": "testuser", "password": "testing"})
    assert auth_user_response.status_code == 200

    food_data = {
        "name": "apple",
        "date": "2023-06-18",
        "time": "07:55:13",
        "quantity": 1,
        "calories": "95"
    }

    # Act
    access_token = auth_user_response.json()["access_token"]
    response = client.post(
        f"/food/testuser/new_food?auth_token={access_token}",
        json=food_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "apple"
    assert response.json()["date"] == "2023-06-18"
    assert response.json()["time"] == "1900-01-01 07:55:13"
    assert response.json()["quantity"] == 1
    assert response.json()["calories"] == 95

# test to get all food for a user
def test_get_all_food(client):
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
