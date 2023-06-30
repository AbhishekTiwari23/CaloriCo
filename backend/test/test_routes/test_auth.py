def test_create_user(client):
    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "JohnDoe@123",
        "join_date": "2021-01-01",
        "role": "USER",
        "expected_calories": 2000

    }

    # Act
    response = client.post("/auth/SighUp", json=user_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["first_name"] == "JOHN"
    assert response.json()["last_name"] == "DOE"
    assert response.json()["username"] == "TESTUSER"
    assert response.json()["email"] == "TESTUSER@GMAIL.COM"
    assert response.json()["password"] != "JohnDoe@123"
    assert response.json()["join_date"] == "2021-01-01"
    assert response.json()["role"] == "USER"
    assert response.json()["expected_calories"] == 2000

# test for duplicate username and email
def test_create_user_duplicate_username(client):
    # Arrange
    existing_user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "test@email.com",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "USER",
        "expected_calories": 2000
    }
    response_existing_user = client.post("/auth/SighUp", json=existing_user_data)  # Create an existing user

    # Act
    user_data = {
         "first_name": "JOHN",
        "last_name": "DOE",
        "username": "TESTUSER",
        "email": "TEST@EMAIL.COM",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "USER",
        "expected_calories": 2000
    }
    response = client.post("/auth/SighUp", json=user_data)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "User with email TEST@EMAIL.COM or username TESTUSER already exists"


# test for login with correct credentials
def test_login(client):
    # Arrange
    user_data = {
         "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "test@email.com",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "USER",
        "expected_calories": 2000
    }
    response_existing_user = client.post("/auth/SighUp", json=user_data)  # Create an existing user

    # Act
    response = client.post("/auth/token", data={"username": "TESTUSER", "password": "Testing@123"})

    # Assert
    assert response.status_code == 200
    assert response.json()["access_token"] != None
    assert response.json()["token_type"] == "bearer"

# test for login with incorrect credentials
def test_login_incorrect_credentials(client):
    # Arrange
    user_data = {
         "first_name": "John",
        "last_name": "Doe",
        "username": "testuser",
        "email": "test@email.com",
        "password": "Testing@123",
        "join_date": "2021-01-01",
        "role": "USER",
        "expected_calories": 2000
    }
    response_existing_user = client.post("/auth/SighUp", json=user_data)  # Create an existing user

    # Act
    response = client.post("/auth/token", data={"username": "testur", "password": "Testing@123"})

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


# test for login with non existing user
def test_login_non_existing_user(client):
    # Act
    response = client.post("/auth/token", data={"username": "testur", "password": "Testing@123"})

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"