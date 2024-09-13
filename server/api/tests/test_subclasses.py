from fastapi.testclient import TestClient

from server.database.models.classes import Class, Subclass

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


def test_subclass_name_put(create_subclass, db_session):
    response = client.put(
        f"/api/subclasses/{create_subclass.id}",
        json={"subclass_name": "Armourer"},
    )
    subclass = db_session.query(Subclass).first()
    assert response.status_code == 200
    assert subclass.name == "Armourer"
    assert response.json() == {
        "message": "Subclass 'Armourer' has been updated.",
        "subclass": {"id": 1, "class_id": 1, "name": "Armourer"},
    }


def test_subclass_class_put(create_subclass, db_session):
    cls = Class(name="Barbarian")
    db_session.add(cls)
    db_session.commit()
    response = client.put(
        f"/api/subclasses/{create_subclass.id}",
        json={"class_id": cls.id},
    )
    subclass = db_session.query(Subclass).first()
    assert response.status_code == 200
    assert subclass.class_id == 2
    assert response.json() == {
        "message": "Subclass 'Alchemist' has been updated.",
        "subclass": {"id": 1, "class_id": 2, "name": "Alchemist"},
    }


def test_subclass_wrong_class_put(create_subclass, db_session):
    response = client.put(
        f"/api/subclasses/{create_subclass.id}",
        json={"class_id": 2},
    )
    subclass = db_session.query(Subclass).first()
    assert response.status_code == 404
    assert subclass.class_id == 1
    assert response.json() == {
        "detail": "The class you are trying to link to this subclass does not exist."
    }


def test_fake_subclass_put(create_subclass, db_session):
    response = client.put(
        "/api/subclasses/2",
        json={"subclass_name": "Armourer"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The subclass you are trying to update does not exist.",
    }


def test_subclass_delete(create_subclass, db_session):
    response = client.delete(f"/api/subclasses/{create_subclass.id}")
    subclass = (
        db_session.query(Subclass).filter(Subclass.id == create_subclass.id).first()
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Subclass has been deleted."}
    assert subclass == None


def test_subclass_delete(create_subclass, db_session):
    response = client.delete(f"/api/subclasses/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The subclass you are trying to delete does not exist."
    }
