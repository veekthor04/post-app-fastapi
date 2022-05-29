import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app import schemas
from app.config import settings

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY


def test_root(client: TestClient):
    res = client.get("/")
    assert res.status_code == 200


def test_create_user(client: TestClient):
    res = client.post(
        "/users/", json={"email": "admin@12345.com", "password": "pass123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "admin@12345.com"
    assert res.status_code == 201


def test_login_user(client: TestClient, sample_user: dict):
    res = client.post(
        "/login/",
        data={
            "username": sample_user["email"],
            "password": sample_user["password"],
        },
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM]
    )
    id = payload.get("user_id")
    assert id == sample_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "pass123", 403),
        ("admin@12345.com", "wrong_password", 403),
        ("wrongemail@gmail.com", "wrong_password", 403),
        (None, "pass123", 422),
        ("admin@12345.com", None, 422),
    ],
)
def test_incorrect_login(
    client: TestClient, email: str, password: str, status_code: str
):
    res = client.post(
        "/login/",
        data={
            "username": email,
            "password": password,
        },
    )

    assert res.status_code == status_code
