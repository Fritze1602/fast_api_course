from fastapi.testclient import TestClient
from app.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.oauth2 import create_access_token
from app import models

from app.database import get_db, Base
import pytest

# Test Database
SQLALCHEMY_DATABASE_URL = f"postgresql://{get_settings().database_username}:{get_settings().database_password}@{get_settings().database_hostname}:{get_settings().database_port}/{get_settings().database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# ***************************
# ****  4 Authorization *****
# ***************************


@pytest.fixture
def test_users(client):
    user_data = [
        {"email": "fs@exovia.com", "password": "password123"},
        {"email": "jw@exovia.com", "password": "password123"}
    ]

    responsesJSON = list(map(lambda user: client.post("/users", json=user).json(), user_data))

    return responsesJSON
    # res = client.post("/users/", json=user_data)

    # assert res.status_code == 201

    # new_user = res.json()
    # new_user['password'] = user_data['password']
    # return new_user


@pytest.fixture
def tokens(test_users):
    tokens = list(map(
        lambda test_user: create_access_token({"user_id": test_user['id']}), test_users))
    return tokens


@pytest.fixture
def authorized_clients(client, tokens):
    def get_client_with_header(id):
        client.headers = {
            ** client.headers,
            "Authorization": f"Bearer {tokens[id]}"
        }
        return client

    # client.headers = {
    #     ** client.headers,
    #     "Authorization": f"Bearer {tokens[0]}"
    # }
    return get_client_with_header

# ***************************
# *****  Example Posts ******
# ***************************


@pytest.fixture
def test_posts(test_users, session):
    post_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_users[0]['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_users[0]['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_users[1]['id']
    }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
