from sqlalchemy import select

from server.models import Class
from .conftest import client


def test_no_auth_classes():
    response = client.get("/api/classes")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_classes(login, create_class):
    token = login.get(name="user_token")
    response = client.get("/api/classes", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Artificer", "subclasses": []}]


def test_get_no_classes(login):
    token = login.get(name="user_token")
    response = client.get("/api/classes", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == []


def test_get_class(login, create_class):
    token = login.get(name="user_token")
    response = client.get("/api/classes/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Artificer",
        "subclasses": [],
    }


def test_get_no_class(login):
    token = login.get(name="user_token")
    response = client.get("/api/classes/2", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found."}


def test_post_class(login):
    token = login.get(name="user_token")
    response = client.post("/api/classes", headers={"Authorization": f"Bearer {token}"}, json={"class_name": "Test"})

    assert response.status_code == 201
    assert response.json() == {
        "message": "New class 'Test' has been added to the database.",
        "cls": {
            "name": "Test",
            "id": 1,
            "subclasses": [],
        },
    }


def test_post_duplicate_class(login):
    token = login.get(name="user_token")
    client.post("/api/classes", json={"class_name": "Test"}, headers={"Authorization": f"Bearer {token}"})
    response = client.post("/api/classes", json={"class_name": "Test"}, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Class already exists."}


def test_class_name_put(login, create_class, db_session):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/classes/{create_class.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"class_name": "Barbarian"},
    )

    stmt = select(Class)
    cls = db_session.execute(stmt).scalar_one_or_none()

    assert response.status_code == 200
    assert cls.name == "Barbarian"
    assert response.json() == {
        "message": "Class 'Barbarian' has been updated.",
        "cls": {"id": 1, "name": "Barbarian", "subclasses": []},
    }


def test_class_duplicate_name_put(login, create_class, db_session):
    cls = Class(name="Barbarian")
    db_session.add(cls)
    db_session.commit()

    token = login.get(name="user_token")
    response = client.put(
        f"/api/classes/{cls.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"class_name": "Artificer"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_fake_class_put(login, create_class):
    token = login.get(name="user_token")
    response = client.put(
        "/api/classes/2",
        headers={"Authorization": f"Bearer {token}"},
        json={"class_name": "Barbarian"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The class you are trying to update does not exist.",
    }


def test_class_delete(login, create_class, db_session):
    token = login.get(name="user_token")
    response = client.delete(f"/api/classes/{create_class.id}", headers={"Authorization": f"Bearer {token}"})

    cls = db_session.get(Class, create_class.id)

    assert response.status_code == 200
    assert response.json() == {"message": "Class has been deleted."}
    assert cls is None


def test_class_fake_delete(login, create_class):
    token = login.get(name="user_token")
    response = client.delete(f"/api/classes/2", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The class you are trying to delete does not exist."
    }
