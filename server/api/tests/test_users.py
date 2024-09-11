from fastapi.testclient import TestClient

from .conftest import app

client = TestClient(app)


def test_get_users(create_user, db_session):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json() == {
        "users": [{"name": "test", "password": None, "id": 1, "image": None}]
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
        "image": None,
        "parties": [{"name": "Murder Hobo Party", "id": 1}],
        "roles": [{"id": 1, "name": "Player"}],
        "characters": [],
    }


def test_get_no_user(create_user, db_session):
    response = client.get("/api/users/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}
