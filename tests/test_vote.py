import pytest
from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models, schemas


@pytest.fixture
def sample_vote(
    sample_posts: List[models.Post], sample_user: dict, session: Session
):
    new_vote = models.Vote(
        post_id=sample_posts[0].id, user_id=sample_user["id"]
    )
    session.add(new_vote)
    session.commit()


def test_vote_on_post(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    res = authorized_client.post(
        "/vote/", json={"post_id": sample_posts[0].id, "dir": 1}
    )
    assert res.status_code == 201


def test_vote_twice_on_post(
    authorized_client: TestClient, sample_posts: List[models.Post], sample_vote
):
    res = authorized_client.post(
        "/vote/", json={"post_id": sample_posts[0].id, "dir": 1}
    )
    assert res.status_code == 409


def test_delete_vote_on_post(
    authorized_client: TestClient, sample_posts: List[models.Post], sample_vote
):
    res = authorized_client.post(
        "/vote/", json={"post_id": sample_posts[0].id, "dir": 0}
    )
    assert res.status_code == 201


def test_delete_vote_on_post_non_exist(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    res = authorized_client.post(
        "/vote/", json={"post_id": sample_posts[0].id, "dir": 0}
    )
    assert res.status_code == 404


def test_vote_on_post_non_exist(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    res = authorized_client.post("/vote/", json={"post_id": 123, "dir": 1})
    assert res.status_code == 404


def test_unauthorized_user_vote_post_post(
    client: TestClient, sample_posts: List[models.Post]
):
    res = client.post("/vote/", json={"post_id": sample_posts[0].id, "dir": 1})
    assert res.status_code == 401
