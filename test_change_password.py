from app import app

client = app.test_client()
register_path = "/register"
password_path = "/changePassword"


def test_setup():
    data = {"username": "change_password_user123", "password": "aa123456", "confirmation": "aa123456"}
    client.post(register_path, data=data)


def test_passqord_get():
    response = client.get(password_path)
    assert response.status_code == 200


def test_passqord():
    data = {"current_password": "aa123456", "new_password": "aa111111", "confirmation": "aa111111"}
    response = client.post(password_path, data=data)
    assert response.status_code == 302