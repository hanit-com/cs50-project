from app import app

client = app.test_client()


def test_registration_get():
    response = client.get("/register")
    assert response.status_code == 200


def test_registration_post():
    data = {"username": "user222", "password": "123456", "confirmation": "123456"}
    response = client.post("/register", data=data)
    assert response.status_code == 302


def test_login_get():
    response = client.get("/login")
    assert response.status_code == 200


def test_login_post():
    data = {"username": "user222", "password": "123456"}
    response = client.post("/login", data=data)
    assert response.status_code == 302


def test_index():
    response = client.get("/")
    assert response.status_code == 200

def test_passqord_get():
    response = client.get("/changePassword")
    assert response.status_code == 200


def test_passqord_post():
    data = {"current_password": "123456", "new_password": "111111", "confirmation": "111111"}
    response = client.post("/changePassword", data=data)
    assert response.status_code == 302


def test_logout():
    client.post("/logout")
    response = client.get("/")
    assert response.status_code == 302