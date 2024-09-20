from fastapi.testclient import TestClient

from server.database.models.damage_types import DamageType

from .conftest import app

client = TestClient(app)


def test_get_damage_types(create_damage_type, db_session):
    response = client.get("/api/damage_types")
    assert response.status_code == 200
    assert response.json() == {
        "damage_types": [
            {"id": 1, "name": "Fire"},
        ]
    }


def test_get_no_users(db_session):
    response = client.get("/api/damage_types")
    assert response.status_code == 404
    assert response.json() == {"detail": "No damage_types found."}


def test_get_damage_type(create_damage_type, db_session):
    response = client.get("/api/damage_types/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Fire"}


def test_get_no_damage_type(create_damage_type, db_session):
    response = client.get("/api/damage_types/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_damage_type(db_session):
    response = client.post(
        "/api/damage_types",
        json={
            "damage_type_name": "Fire",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New damage_type 'Fire' has been added to the database.",
        "damage_type": {"id": 1, "name": "Fire"},
    }


def test_post_duplicate_damage_type(db_session):
    client.post(
        "/api/damage_types",
        json={
            "damage_type_name": "Fire",
        },
    )
    response = client.post(
        "/api/damage_types",
        json={
            "damage_type_name": "Fire",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Damage type already exists."}


def test_damage_type_name_put(create_damage_type, db_session):
    response = client.put(
        f"/api/damage_types/{create_damage_type.id}",
        json={"damage_type_name": "Slashing"},
    )
    damage_type = db_session.query(DamageType).first()
    assert response.status_code == 200
    assert damage_type.name == "Slashing"
    assert response.json() == {
        "message": "Damage type 'Slashing' has been updated.",
        "damage_type": {"id": 1, "name": "Slashing"},
    }


def test_damage_type_duplicate_name_put(create_damage_type, db_session):
    damage_type = DamageType(name="Slashing")
    db_session.add(damage_type)
    db_session.commit()
    response = client.put(
        f"/api/damage_types/{damage_type.id}",
        json={"damage_type_name": "Fire"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_damage_type_fake_damage_type_put(create_race, create_damage_type, db_session):
    response = client.put(
        "/api/damage_types/2",
        json={"damage_type_name": "Slashing"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The damage_type you are trying to update does not exist.",
    }


def test_damage_type_delete(create_damage_type, db_session):
    response = client.delete(f"/api/damage_types/{create_damage_type.id}")
    damage_type = (
        db_session.query(DamageType)
        .filter(DamageType.id == create_damage_type.id)
        .first()
    )
    assert response.status_code == 200
    assert response.json() == {"message": f"Damage type has been deleted."}
    assert damage_type == None


def test_damage_type_fake_delete(create_damage_type, db_session):
    response = client.delete(f"/api/damage_types/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The damage_type you are trying to delete does not exist."
    }
