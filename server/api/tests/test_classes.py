from fastapi.testclient import TestClient

from server.database.models.classes import Class

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
        "message": "New class 'Test' has been added to the database.",
        "class": {"name": "Test", "id": 1},
    }


def test_post_duplicate_class(db_session):
    client.post("/api/classes", json={"class_name": "Test"})
    response = client.post("/api/classes", json={"class_name": "Test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Class already exists."}


def test_class_name_put(create_class, db_session):
    response = client.put(
        f"/api/classes/{create_class.id}",
        json={"class_name": "Barbarian"},
    )
    cls = db_session.query(Class).first()
    assert response.status_code == 200
    assert cls.name == "Barbarian"
    assert response.json() == {
        "message": "Class 'Barbarian' has been updated.",
        "class": {"id": 1, "name": "Barbarian"},
    }


def test_fake_class_put(create_class, db_session):
    response = client.put(
        "/api/classes/2",
        json={"class_name": "Barbarian"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The class you are trying to update does not exist.",
    }


def test_class_delete(create_class, db_session):
    response = client.delete(f"/api/classes/{create_class.id}")
    cls = db_session.query(Class).filter(Class.id == create_class.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": "class has been deleted."}
    assert cls == None


def test_class_delete(create_class, db_session):
    response = client.delete(f"/api/classes/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The class you are trying to delete does not exist."
    }
