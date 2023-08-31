
from app import schemas
from app.config import get_settings

from jose import jwt
import pytest


@pytest.fixture
def test_user(client):
    user_data = {"email": "test__fs@exovia.de", "password": "password123"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

# def test_root(client):
#     res = client.get("/")
#     msg = (res.json().get('message'))
#     assert msg == "Hello World!!!"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users", json={"email": "test__fs@exovia.de", "password": "password123"})
    # validation against the schema
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test__fs@exovia.de"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, get_settings(
    ).secret_key, algorithms=[get_settings().algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('test__fs@exovia.de', 'wront_Password123', 403),
    ('wrongemail@gmail.com', 'wront_Password123', 403),
    (None, 'wront_Password123', 422),
    ('test__fs@exovia.de', None, 422)

])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get('detail') == 'Invalid credentials'
