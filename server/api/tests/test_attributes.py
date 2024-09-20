from fastapi.testclient import TestClient

from server.database.models.attributes import Attribute

from .conftest import app

client = TestClient(app)


def test_get_attributes(create_attribute, db_session):
    response = client.get("/api/attributes")
    assert response.status_code == 200
    assert response.json() == {
        "attributes": [
            {"id": 1, "name": "Charmed"},
        ]
    }


def test_get_no_users(db_session):
    response = client.get("/api/attributes")
    assert response.status_code == 404
    assert response.json() == {"detail": "No attributes found."}


def test_getattribute(create_attribute, db_session):
    response = client.get("/api/attributes/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Charmed"}


def test_get_no_attribute(create_attribute, db_session):
    response = client.get("/api/attributes/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_attribute(db_session):
    response = client.post(
        "/api/attributes",
        json={
            "attribute_name": "Charmed",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New attribute 'Charmed' has been added to the database.",
        "attribute": {"id": 1, "name": "Charmed"},
    }


def test_post_duplicate_attribute(db_session):
    client.post(
        "/api/attributes",
        json={
            "attribute_name": "Charmed",
        },
    )
    response = client.post(
        "/api/attributes",
        json={
            "attribute_name": "Charmed",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Damage type already exists."}


def test_attribute_name_put(create_attribute, db_session):
    response = client.put(
        f"/api/attributes/{create_attribute.id}",
        json={"attribute_name": "Slashing"},
    )
    attribute = db_session.query(Attribute).first()
    assert response.status_code == 200
    assert attribute.name == "Slashing"
    assert response.json() == {
        "message": "Damage type 'Slashing' has been updated.",
        "attribute": {"id": 1, "name": "Slashing"},
    }


def test_attribute_duplicate_name_put(create_attribute, db_session):
    attribute = Attribute(name="Slashing")
    db_session.add(attribute)
    db_session.commit()
    response = client.put(
        f"/api/attributes/{attribute.id}",
        json={"attribute_name": "Charmed"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_attribute_fake_attribute_put(create_race, create_attribute, db_session):
    response = client.put(
        "/api/attributes/2",
        json={"attribute_name": "Slashing"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The attribute you are trying to update does not exist.",
    }


def test_attribute_delete(create_attribute, db_session):
    response = client.delete(f"/api/attributes/{create_attribute.id}")
    attribute = (
        db_session.query(Attribute).filter(Attribute.id == create_attribute.id).first()
    )
    assert response.status_code == 200
    assert response.json() == {"message": f"Damage type has been deleted."}
    assert attribute == None


def test_attribute_fake_delete(create_attribute, db_session):
    response = client.delete(f"/api/attributes/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The attribute you are trying to delete does not exist."
    }
