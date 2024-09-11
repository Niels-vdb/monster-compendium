from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_roles(create_role, db_session):
    response = client.get("/api/roles")
    assert response.status_code == 200
    assert response.json() == {
        "roles": [
            {"id": 1, "name": "Player"},
        ]
    }


def test_get_no_roles(db_session):
    response = client.get("/api/roles")
    assert response.status_code == 404
    assert response.json() == {"detail": "No roles found."}


def test_get_role(create_role, db_session):
    response = client.get("/api/roles/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Player",
        "users": [],
    }


def test_get_no_role(create_role, db_session):
    response = client.get("/api/roles/1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found."}
