from fastapi.testclient import TestClient
from sqlalchemy import select

from server.models import Class
from server.models import Subclass

from .conftest import app


client = TestClient(app)


def test_get_subclasses(create_subclass, db_session):
    response = client.get("/api/subclasses")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Alchemist",
            "parent_class": {"id": 1, "name": "Artificer"},
        }
    ]


def test_get_no_subclasses(db_session):
    response = client.get("/api/subclasses")
    assert response.status_code == 200
    assert response.json() == []


def test_get_subclass(create_subclass, db_session):
    response = client.get("/api/subclasses/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alchemist",
        "parent_class": {"id": 1, "name": "Artificer"},
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
    assert response.status_code == 201
    assert response.json() == {
        "message": "New subclass 'Alchemist' has been added to the database.",
        "subclass": {
            "id": 1,
            "name": "Alchemist",
            "parent_class": {"id": 1, "name": "Artificer"},
        },
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


def test_subclass_put(create_subclass, db_session):
    cls = Class(name="Barbarian")
    db_session.add(cls)
    db_session.commit()

    response = client.put(
        f"/api/subclasses/{create_subclass.id}",
        json={"subclass_name": "Armourer", "class_id": cls.id},
    )
    stmt = select(Subclass)
    subclass = db_session.execute(stmt).scalar_one_or_none()
    assert response.status_code == 200
    assert subclass.name == "Armourer"
    assert subclass.class_id == 2
    assert response.json() == {
        "message": "Subclass 'Armourer' has been updated.",
        "subclass": {
            "id": 1,
            "name": "Armourer",
            "parent_class": {"id": 2, "name": "Barbarian"},
        },
    }


def test_subclass_duplicate_name_put(create_class, create_subclass, db_session):
    subclass = Subclass(name="Armourer", class_id=1)
    db_session.add(subclass)
    db_session.commit()
    response = client.put(
        f"/api/subclasses/{subclass.id}",
        json={"subclass_name": "Alchemist"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_subclass_wrong_class_put(create_subclass, db_session):
    response = client.put(
        f"/api/subclasses/{create_subclass.id}",
        json={"class_id": 2},
    )
    stmt = select(Subclass)
    subclass = db_session.execute(stmt).scalar_one_or_none()
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
    subclass = db_session.get(Subclass, create_subclass.id)
    assert response.status_code == 200
    assert response.json() == {"message": "Subclass has been deleted."}
    assert subclass == None


def test_subclass_fake_delete(create_subclass, db_session):
    response = client.delete(f"/api/subclasses/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The subclass you are trying to delete does not exist."
    }
