from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_classes(create_class, db_session):
    response = client.get("/api/classes")
    assert response.status_code == 200
    assert response.json() == {
        "classes": [
            {"id": 1, "name": "Artificer"},
        ]
    }


def test_get_no_classes(db_session):
    response = client.get("/api/classes")
    assert response.status_code == 404
    assert response.json() == {"detail": "No classes found."}


def test_get_class(create_class, db_session):
    response = client.get("/api/classes/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Artificer",
        "subclasses": [],
    }


def test_get_no_class(db_session):
    response = client.get("/api/classes/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found."}


def test_post_class(db_session):
    response = client.post("/api/classes", json={"class_name": "Test"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "New class 'Test' has been added tot he database.",
        "class": {"name": "Test", "id": 1},
    }


def test_post_duplicate_class(db_session):
    client.post("/api/classes", json={"class_name": "Test"})
    response = client.post("/api/classes", json={"class_name": "Test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Class already exists."}
