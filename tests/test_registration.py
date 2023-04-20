from app import app

client = app.test_client()
register_path = "/register"


def test_registration_get():
    response = client.get(register_path)
    assert response.status_code == 200


def test_registration_short_username():
    data = {"username": "user", "password": "aa123456", "confirmation": "aa123456"}
    response = client.post(register_path, data=data)
    assert response.status_code == 400


def test_registration_no_letter_username():
    data = {"username": "00000", "password": "aa123456", "confirmation": "aa123456"}
    response = client.post(register_path, data=data)
    assert response.status_code == 400


def test_registration_no_digit_username():
    data = {"username": "useruser", "password": "aa123456", "confirmation": "aa123456"}
    response = client.post(register_path, data=data)
    assert response.status_code == 400


def test_registration_short_password():
    data = {"username": "user123", "password": "aa", "confirmation": "aa"}
    response = client.post(register_path, data=data)
    assert response.status_code == 400

def test_registration_no_letter_password():
    data = {"username": "00000", "password": "123456", "confirmation": "123456"}
    response = client.post(register_path, data=data)
    assert response.status_code == 400


def test_registration_no_digit_password():
    data = {"username": "useruser", "password": "password", "confirmation": "password"}
    response = client.post(register_path, data=data)
    assert response.status_code == 400


def test_registration_passwords_dont_match():
    data = {"username": "user123", "password": "aa123456", "confirmation": "aa654321"}
    response = client.post(register_path, data=data)
    assert response.status_code == 400


def test_registration_missing_parameters():
    missing_username_data = {"password": "aa123456", "confirmation": "aa123456"}
    missing_password_data = {"username": "user123", "confirmation": "aa123456"}
    missing_confirmation_data = {"username": "user123", "password": "aa123456"}

    missing_username_response = client.post(register_path, data=missing_username_data)
    assert missing_username_response.status_code == 400
    missing_password_response = client.post(register_path, data=missing_password_data)
    assert missing_password_response.status_code == 400
    missing_confirmation_response = client.post(register_path, data=missing_confirmation_data)
    assert missing_confirmation_response.status_code == 400


def test_registration_username_taken():
    taken_user_data = {"username": "taken_user123", "password": "aa123456", "confirmation": "aa123456"}
    client.post(register_path, data=taken_user_data)

    data = {"username": "taken_user123", "password": "aa123456", "confirmation": "aa123456"}
    response = client.post(register_path, data=data)
    assert response.status_code == 400


def test_registration():
    data = {"username": "user_success123", "password": "aa123456", "confirmation": "aa123456"}
    response = client.post(register_path, data=data)
    assert response.status_code == 302