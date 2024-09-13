from fastapi.testclient import TestClient

from .conftest import app

client = TestClient(app)


def test_get_users(create_user, db_session):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "password": None,
                "username": "Test",
                "name": "test",
                "image": None,
            }
        ]
    }


def test_get_no_users(db_session):
    response = client.get("/api/users")
    assert response.status_code == 404
    assert response.json() == {"detail": "No users found."}


def test_get_user(create_user, db_session):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "test",
        "username": "Test",
        "image": None,
        "parties": [{"name": "Murder Hobo Party", "id": 1}],
        "roles": [{"id": 1, "name": "Player"}],
        "characters": [],
    }


def test_get_no_user(create_user, db_session):
    response = client.get("/api/users/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


def test_post_user(create_party, create_role, create_pc, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [1],
            "characters": [1],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New user 'Player' has been added to the database.",
        "user": {
            "id": 2,
            "password": None,
            "username": "player",
            "name": "Player",
            "image": None,
        },
    }


def test_post_duplicate_user(create_party, create_role, create_pc, db_session):
    client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [1],
            "characters": [1],
        },
    )
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [1],
            "characters": [1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists."}


def test_post_user_fake_party(create_party, create_role, create_pc, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [2],
            "roles": [1],
            "characters": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party, role or character you are trying to bind to this race does not exist."
    }


def test_post_user_fake_role(create_party, create_role, create_pc, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [2],
            "characters": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party, role or character you are trying to bind to this race does not exist."
    }


def test_post_user_fake_character(create_party, create_role, create_pc, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [1],
            "characters": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party, role or character you are trying to bind to this race does not exist."
    }
