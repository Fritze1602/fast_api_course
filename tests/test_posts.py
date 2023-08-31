from typing import List
from app import schemas
from pydantic import TypeAdapter
import pytest
from fastapi import status


def test_get_all_posts(authorized_clients, test_posts):

    res = authorized_clients(0).get("/posts")
    posts = res.json()
    ta = TypeAdapter(List[schemas.PostOut])
    assert ta.validate_python(posts)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_authorized_user_get_one_posts(authorized_clients, test_posts):
    res = authorized_clients(0).get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content
    assert post.id == test_posts[0].id
    assert post.owner_id == test_posts[0].owner_id
    assert res.status_code == 200


def test_get_one_post_not_exist(authorized_clients, test_posts):
    res = authorized_clients(0).get("/posts/88888")
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("terroristica", "Carsten Hoppe is drunken", True),
    ("dark end of the street", "Robert Palmer is alive", False),
    ("stuss", "edeldark must be refined", True)
])
def test_create_posts(authorized_clients, test_posts, test_users, title, content, published):
    res = authorized_clients(0).post("/posts", json={
        "title": title,
        "content": content,
        "published": published,
        "owner_id": test_users[0]["id"]
    })
    created_post = schemas.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert res.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize("title, content, published, status_exp", [
    ("stuss", "edeldark must be refined", True, status.HTTP_401_UNAUTHORIZED)
])
def test_unauthorized_user_create_posts(client, test_posts, test_users, title, content, published, status_exp):
    res = client.post("/posts", json={
        "title": title,
        "content": content,
        "published": published,
        "owner_id": test_users[0]["id"]
    })
    assert res.status_code == status_exp


def test_create_post_default_published_true(authorized_clients, test_posts):
    res = authorized_clients(0).post("/posts", json={
        "title": 'arbitraty title',
        "content": 'arbitraty content',
    })
    created_post = schemas.Post(**res.json())
    assert created_post.title == 'arbitraty title'
    assert created_post.content == 'arbitraty content'
    assert created_post.published == True


def test_unauthorized_user_delete_posts(client, test_posts,):
    post_id = test_posts[0].id
    res = client.delete(f"/posts/{post_id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_delete_posts(authorized_clients, test_posts,):
    post_id = test_posts[1].id
    res = authorized_clients(0).delete(f"/posts/{post_id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_deleting_unexisting_posts(authorized_clients, test_posts):
    post_id = 99999
    res = authorized_clients(0).delete(f"/posts/{post_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_user_post(authorized_clients, test_posts):
    post_id = test_posts[2].id
    res = authorized_clients(0).delete(f"/posts/{post_id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_clients, test_posts):
    post_id = test_posts[1].id
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False
    }
    res = authorized_clients(0).put(f"/posts/{post_id}", json=data)
    updatedPost = schemas.Post(**res.json())
    assert updatedPost.title == data['title']
    assert updatedPost.content == data['content']
    assert updatedPost.published == data['published']
    assert res.status_code == status.HTTP_201_CREATED


def test_update_another_users_post(authorized_clients, test_posts):
    post_id = test_posts[2].id
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False
    }
    res = authorized_clients(0).put(f"/posts/{post_id}", json=data)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_other_user_post(authorized_clients, test_posts):
    post_id = test_posts[2].id
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False
    }
    res = authorized_clients(0).put(f"/posts/{post_id}", json=data)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_unexisting_post(authorized_clients, test_posts):
    post_id = 99999999
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False
    }
    res = authorized_clients(0).put(f"/posts/{post_id}", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND
