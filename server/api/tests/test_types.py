from fastapi.testclient import TestClient
from sqlalchemy import select

from server.database.models.characteristics import Type

from .conftest import app


client = TestClient(app)


def test_get_types(create_type, db_session):
    response = client.get("/api/types")
    assert response.status_code == 200
    assert response.json() == [{"name": "Aberration", "id": 1}]


def test_get_no_types(db_session):
    response = client.get("/api/types")
    assert response.status_code == 200
    assert response.json() == []


def test_get_type(create_type, db_session):
    response = client.get("/api/types/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Aberration"}


def test_get_no_type(create_type, db_session):
    response = client.get("/api/types/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Type not found."}


def test_post_type(db_session):
    response = client.post(
        "/api/types",
        json={
            "type_name": "Humanoid",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "message": "New type 'Humanoid' has been added to the database.",
        "type": {"id": 1, "name": "Humanoid"},
    }


def test_post_duplicate_type(db_session):
    client.post(
        "/api/types",
        json={
            "type_name": "Humanoid",
        },
    )
    response = client.post(
        "/api/types",
        json={
            "type_name": "Humanoid",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Type already exists."}


def test_type_name_put(create_type, db_session):
    response = client.put(
        f"/api/types/{create_type.id}",
        json={"type_name": "Celestial"},
    )
    stmt = select(Type)
    type = db_session.execute(stmt).scalar_one_or_none()
    assert response.status_code == 200
    assert type.name == "Celestial"
    assert response.json() == {
        "message": "type 'Celestial' has been updated.",
        "type": {"id": 1, "name": "Celestial"},
    }


def test_type_duplicate_name_put(create_type, db_session):
    type = Type(name="Celestial")
    db_session.add(type)
    db_session.commit()
    response = client.put(
        f"/api/types/{type.id}",
        json={"type_name": "Aberration"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_type_fake_type_put(create_race, create_type, db_session):
    response = client.put(
        "/api/types/2",
        json={"type_name": "Celestial"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The type you are trying to update does not exist.",
    }


def test_type_delete(create_type, db_session):
    response = client.delete(f"/api/types/{create_type.id}")
    type = db_session.get(Type, create_type.id)
    assert response.status_code == 200
    assert response.json() == {"message": f"Type has been deleted."}
    assert type == None


def test_type_fake_delete(create_type, db_session):
    response = client.delete(f"/api/types/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The type you are trying to delete does not exist."
    }
