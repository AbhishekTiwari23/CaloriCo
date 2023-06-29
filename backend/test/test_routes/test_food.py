from core.calories import get_calories
import json
# test to create a new food
def test_create_new_food(client):
    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "ADMIN",
        "expected_calories": 2000
    }

    create_user_response = client.post("/auth/SighUp", json=user_data)
    assert create_user_response.status_code == 200
    auth_user_response = client.post("/auth/token", data={"username": "TESTUSER", "password": "Testing@123"})
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
        f"/food/TESTUSER/new_food?auth_token={access_token}",
        json=food_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "APPLE"
    assert response.json()["date"] == "2023-06-18"
    assert response.json()["time"] == "1900-01-01 07:55:13"
    assert response.json()["quantity"] == 1
    assert response.json()["calories"] == 95

# test to create a new food
def test_create_new_food_not_calory(client):
    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "ADMIN",
        "expected_calories": 2000
    }

    create_user_response = client.post("/auth/SighUp", json=user_data)
    assert create_user_response.status_code == 200
    auth_user_response = client.post("/auth/token", data={"username": "TESTUSER", "password": "Testing@123"})
    assert auth_user_response.status_code == 200

    food_data = {
        "name": "apple",
        "date": "2023-06-18",
        "time": "07:55:13",
        "quantity": 1,
        "calories": ""
    }

    # Act
    access_token = auth_user_response.json()["access_token"]
    response = client.post(
        f"/food/TESTUSER/new_food?auth_token={access_token}",
        json=food_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    add_calories = response.json()["calories"]
    if not response.json()["calories"]:
            api_response = get_calories(food_data["name"], food_data["quantity"])
            data = json.loads(api_response)
            add_calories = data['items'][0]['calories']

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "APPLE"
    assert response.json()["date"] == "2023-06-18"
    assert response.json()["time"] == "1900-01-01 07:55:13"
    assert response.json()["quantity"] == 1
    assert response.json()["calories"] == add_calories

#  test to delete a food
def test_delete_food_pos(client):
    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "ADMIN",
        "expected_calories": 2000
    }

    create_user_response = client.post("/auth/SighUp", json=user_data)
    assert create_user_response.status_code == 200
    auth_user_response = client.post("/auth/token", data={"username": "TESTUSER", "password": "Testing@123"})
    assert auth_user_response.status_code == 200

    food_data = {
        "name": "apple",
        "date": "2023-06-18",
        "time": "07:55:13",
        "quantity": 1,
        "calories": ""
    }
    access_token = auth_user_response.json()["access_token"]
    food_entry_response = client.post(
        f"/food/TESTUSER/new_food?auth_token={access_token}",
        json=food_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    food_id = food_entry_response.json()["id"]

    # Act
    response = client.delete(f"/food/delete/{food_id}?&auth_token={access_token}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Food deleted successfully"


#  test to update the food pos
def test_update_food_pos(client):
    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "ADMIN",
        "expected_calories": 2000
    }

    create_user_response = client.post("/auth/SighUp", json=user_data)
    assert create_user_response.status_code == 200
    auth_user_response = client.post("/auth/token", data={"username": "TESTUSER", "password": "Testing@123"})
    assert auth_user_response.status_code == 200

    food_data = {
        "name": "apple",
        "date": "2023-06-18",
        "time": "07:55:13",
        "quantity": 1,
        "calories": "96"
    }
    access_token = auth_user_response.json()["access_token"]
    food_entry_response = client.post(
        f"/food/TESTUSER/new_food?auth_token={access_token}",
        json=food_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    food_id = food_entry_response.json()["id"]
    updated_food_data = {
        "name": "banana",
        "date": "2023-06-18",
        "time": "07:55:13",
        "quantity": 2,
        "calories": "300"
    }
    # Act
    response = client.put(
         f"/food/update/{food_id}?&auth_token={access_token}",
    json=updated_food_data,
    headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "BANANA"
    assert response.json()["date"] == "2023-06-18"
    assert response.json()["time"] == "1900-01-01 07:55:13"
    assert response.json()["quantity"] == 2
    assert response.json()["calories"] == 300

#  test to get all food entries for a user
def test_get_all_food_entries_pos(client):
    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "ADMIN",
        "expected_calories": 2000
    }

    create_user_response = client.post("/auth/SighUp", json=user_data)
    assert create_user_response.status_code == 200
    auth_user_response = client.post("/auth/token", data={"username": "TESTUSER", "password": "Testing@123"})
    assert auth_user_response.status_code == 200
    access_token = auth_user_response.json()["access_token"]

    food_data1 = {
        "name": "apple",
        "date": "2023-06-18",
        "time": "07:55:13",
        "quantity": 1,
        "calories": "96"
    }
    food_entry_response1 = client.post(
        f"/food/TESTUSER/new_food?auth_token={access_token}",
        json=food_data1,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    food_data2 = {
    "name": "banana",
    "date": "2023-06-18",
    "time": "07:55:13",
    "quantity": 1,
    "calories": "96"
}
    food_entry_response2 = client.post(
        f"/food/TESTUSER/new_food?auth_token={access_token}",
        json=food_data2,
        headers={"Authorization": f"Bearer {access_token}"}
)

    food_data3 = {
        "name": "orange",
        "date": "2023-06-18",
        "time": "07:55:13",
        "quantity": 1,
        "calories": "96"
    }
    food_entry_response3 = client.post(
        f"/food/TESTUSER/new_food?auth_token={access_token}",
        json=food_data3,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Act
    response = client.get("/food/{userName}/all?user_name=TESTUSER&auth_token="+access_token)

    # Assert
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3



