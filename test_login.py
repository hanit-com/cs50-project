from app import app

client = app.test_client()
register_path = "/register"
login_path = "/login"
logout_path = "/logout"


# Login


def test_setup():
    data = {"username": "login_user123", "password": "aa123456", "confirmation": "aa123456"}
    client.post(register_path, data=data)


def test_login_get():
    response = client.get(login_path)
    assert response.status_code == 200


def test_login_missing_parameters():
    missing_username_data = {"password": "aa123456"}
    missing_password_data = {"username": "login_user123"}

    missing_username_response = client.post(login_path, data=missing_username_data)
    assert missing_username_response.status_code == 401
    missing_password_response = client.post(login_path, data=missing_password_data)
    assert missing_password_response.status_code == 401


def test_login_incorrect_user():
    data = {"username": "incorrect_user123", "password": "aa123456"}
    response = client.post(login_path, data=data)
    assert response.status_code == 401


def test_login_incorrect_password():
    data = {"username": "login_user123", "password": "xx123456"}
    response = client.post(login_path, data=data)
    assert response.status_code == 401


def test_login():
    data = {"username": "login_user123", "password": "aa123456"}
    response = client.post(login_path, data=data)
    assert response.status_code == 302


# Homepage


def test_index():
    response = client.get("/")
    assert response.status_code == 200


# Logout


def test_logout():
    client.post(logout_path)
    response = client.get("/")
    assert response.status_code == 302