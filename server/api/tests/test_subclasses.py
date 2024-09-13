from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_subclasses(create_subclass, db_session):
    response = client.get("/api/subclasses")
    assert response.status_code == 200
    assert response.json() == {
        "subclasses": [
            {"name": "Alchemist", "class_id": 1, "id": 1},
        ]
    }


def test_get_no_subclasses(db_session):
    response = client.get("/api/subclasses")
    assert response.status_code == 404
    assert response.json() == {"detail": "No subclasses found."}


def test_get_subclass(create_subclass, db_session):
    response = client.get("/api/subclasses/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alchemist",
        "classes": {"name": "Artificer", "id": 1},
    }


def test_get_no_subclass(create_subclass, db_session):
    response = client.get("/api/subclasses/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass not found."}


def test_post_subclass(create_class, db_session):
    response = client.post(
        "/api/subclasses",
        json={"class_id": 1, "subclass_name": "Alchemist"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New subclass 'Alchemist' has been added to the database.",
        "class": {"id": 1, "name": "Alchemist", "class_id": 1},
    }


def test_post_duplicate_subclass(create_class, db_session):
    client.post(
        "/api/subclasses",
        json={"class_id": 1, "subclass_name": "Alchemist"},
    )
    response = client.post(
        "/api/subclasses",
        json={"class_id": 1, "subclass_name": "Alchemist"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Subclass already exists."}


def test_post_subclass_no_class(db_session):
    response = client.post(
        "/api/subclasses",
        json={"class_id": 1, "subclass_name": "Alchemist"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The class you are trying to add a subclass to does not exists."
    }
