from typing import List
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session

from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


DATABASE_URL = f"{settings.DATABASE_URL}_test"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session) -> TestClient:
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def sample_user(client: TestClient) -> dict:
    user_data = {"email": "admin@12345.com", "password": "pass123"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def sample_user_2(client: TestClient) -> dict:
    user_data = {"email": "admin2@12345.com", "password": "pass123"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(sample_user: dict) -> str:
    return create_access_token({"user_id": sample_user["id"]})


@pytest.fixture
def authorized_client(client: TestClient, token: str) -> TestClient:
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def sample_posts(
    sample_user: dict, sample_user_2: dict, session: Session
) -> List[models.Post]:
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": sample_user["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": sample_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": sample_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": sample_user_2["id"],
        },
    ]

    def create_post_model(post: dict) -> models.Post:
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()
    return posts
