from app import schemas
from fastapi import status
import pytest
from app import models


@pytest.fixture
def test_vote(test_posts, session, test_users):
    new_vote = models.Vote(post_id=test_posts[2].id, user_id=test_users[0]['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_clients, test_posts):
    post_id = test_posts[2].id
    data = {
        "post_id": post_id,
        "direction": True
    }
    res = authorized_clients(0).post(f"/votes", json=data)
    assert res.status_code == status.HTTP_201_CREATED


def test_vote_twice(authorized_clients, test_posts, test_vote):
    post_id = test_posts[2].id
    data = {
        "post_id": post_id,
        "direction": True
    }
    res = authorized_clients(0).post(f"/votes", json=data)
    assert res.status_code == status.HTTP_409_CONFLICT


def test_vote_unexisting_post(authorized_clients, test_posts):
    post_id = 888888888
    data = {
        "post_id": post_id,
        "direction": True
    }
    res = authorized_clients(0).post(f"/votes", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_vote_unauthorized_post(client, test_posts):
    post_id = test_posts[2].id
    data = {
        "post_id": post_id,
        "direction": True
    }
    res = client.post(f"/votes", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

# For some reason deleting via json is not supported anymore -> bad practice
# I dont know why. Maybe we should delete via url and without json payloads!
# There are environments which dont allow payloads on delete requests!
# def test_delete_vote(authorized_clients, test_posts, test_vote):
#     post_id = test_posts[2].id
#     data = {
#         "post_id": post_id,
#         "direction": False
#     }
#     res = authorized_clients(0).request("DELETE", "/votes", json=data)
#     print(res)

# def_test_delete_post_doesnt_exist:
#     pass
