from typing import List
from fastapi.testclient import TestClient
import pytest

from app import models, schemas


def test_get_all_posts(client: TestClient, sample_posts: List[models.Post]):
    res = client.get("/posts/")
    assert len(res.json()) == len(sample_posts)
    assert res.status_code == 200


def test_get_one_post_not_exist(
    client: TestClient, sample_posts: List[models.Post]
):
    res = client.get(f"/posts/123/")
    assert res.status_code == 404


def test_get_one_post(client: TestClient, sample_posts: List[models.Post]):
    res = client.get(f"/posts/{sample_posts[0].id}/")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == sample_posts[0].id
    assert post.Post.title == sample_posts[0].title
    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("create first title", "create first content", True),
        ("create second title", "create second content", True),
        ("create third title", "create third content", True),
    ],
)
def test_create_post(
    authorized_client: TestClient,
    sample_user: dict,
    title: str,
    content: str,
    published: bool,
):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published},
    )
    post = schemas.PostOut(**res.json())
    assert post.Post.title == title
    assert post.Post.content == content
    assert post.Post.published == published
    assert post.Post.owner.id == sample_user["id"]
    assert res.status_code == 201


def test_create_post_default_published(authorized_client: TestClient):
    res = authorized_client.post(
        "/posts/",
        json={"title": "title", "content": "content"},
    )
    post = schemas.PostOut(**res.json())
    assert post.Post.published == True
    assert res.status_code == 201


def test_unauthorized_user_create_post(client: TestClient):
    res = client.post(
        "/posts/",
        json={"title": "title", "content": "content"},
    )
    assert res.status_code == 401


def test_delete_post(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    res = authorized_client.delete(f"/posts/{sample_posts[0].id}/")
    assert res.status_code == 204


def test_delete_post_non_exist(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    res = authorized_client.delete(f"/posts/123/")
    assert res.status_code == 404


def test_unauthorized_user_delete_post(
    client: TestClient, sample_posts: List[models.Post]
):
    res = client.delete(f"/posts/{sample_posts[0].id}/")
    assert res.status_code == 401


def test_delete_other_user_post(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    res = authorized_client.delete(f"/posts/{sample_posts[3].id}/")
    assert res.status_code == 403


def test_update_post(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    data = {"title": "updated title", "content": "updated content"}
    res = authorized_client.put(
        f"/posts/{sample_posts[0].id}/",
        json=data,
    )
    post = schemas.PostOut(**res.json())
    assert post.Post.title == data["title"]
    assert post.Post.content == data["content"]
    assert res.status_code == 200


def test_unauthorized_user_update_post(
    client: TestClient, sample_posts: List[models.Post]
):
    data = {"title": "updated title", "content": "updated content"}
    res = client.put(
        f"/posts/{sample_posts[0].id}/",
        json=data,
    )
    assert res.status_code == 401


def test_update_other_user_post(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    data = {"title": "updated title", "content": "updated content"}
    res = authorized_client.put(
        f"/posts/{sample_posts[3].id}/",
        json=data,
    )
    assert res.status_code == 403


def test_update_post_non_exist(
    authorized_client: TestClient, sample_posts: List[models.Post]
):
    data = {"title": "updated title", "content": "updated content"}
    res = authorized_client.put("/posts/123/", json=data)
    assert res.status_code == 404
