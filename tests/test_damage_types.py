from sqlalchemy import select

from server.models import DamageType
from .conftest import client


def test_no_auth_damage_types():
    response = client.get("/api/damage_types")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_damage_types(login, create_damage_type):
    token = login.get(name="user_token")
    response = client.get("/api/damage_types", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Fire"}]


def test_get_no_users(login):
    token = login.get(name="user_token")
    response = client.get("/api/damage_types", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == []


def test_get_damage_type(login, create_damage_type):
    token = login.get(name="user_token")
    response = client.get("/api/damage_types/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Fire"}


def test_get_no_damage_type(login, create_damage_type):
    token = login.get(name="user_token")
    response = client.get("/api/damage_types/2", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_damage_type(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/damage_types",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "damage_type_name": "Fire",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "New damage type 'Fire' has been added to the database.",
        "damage_type": {"id": 1, "name": "Fire"},
    }


def test_post_duplicate_damage_type(login):
    token = login.get(name="user_token")
    client.post(
        "/api/damage_types",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "damage_type_name": "Fire",
        },
    )
    response = client.post(
        "/api/damage_types",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "damage_type_name": "Fire",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Damage type already exists."}


def test_damage_type_put(login, create_damage_type, db_session):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/damage_types/{create_damage_type.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"damage_type_name": "Slashing"},
    )

    stmt = select(DamageType)
    damage_type = db_session.execute(stmt).scalar_one_or_none()

    assert response.status_code == 200
    assert damage_type.name == "Slashing"
    assert response.json() == {
        "message": "Damage type 'Slashing' has been updated.",
        "damage_type": {"id": 1, "name": "Slashing"},
    }


def test_damage_type_duplicate_name_put(login, create_damage_type, db_session):
    damage_type = DamageType(name="Slashing")
    db_session.add(damage_type)
    db_session.commit()

    token = login.get(name="user_token")
    response = client.put(
        f"/api/damage_types/{damage_type.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"damage_type_name": "Fire"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_damage_type_fake_damage_type_put(login, create_race, create_damage_type):
    token = login.get(name="user_token")
    response = client.put(
        "/api/damage_types/2",
        headers={"Authorization": f"Bearer {token}"},
        json={"damage_type_name": "Slashing"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The damage type you are trying to update does not exist.",
    }


def test_damage_type_delete(login, create_damage_type, db_session):
    token = login.get(name="user_token")
    response = client.delete(f"/api/damage_types/{create_damage_type.id}", headers={"Authorization": f"Bearer {token}"})

    damage_type = db_session.get(DamageType, create_damage_type.id)

    assert response.status_code == 200
    assert response.json() == {"message": f"Damage type has been deleted."}
    assert damage_type == None


def test_damage_type_fake_delete(login, create_damage_type):
    token = login.get(name="user_token")
    response = client.delete(f"/api/damage_types/2", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The damage type you are trying to delete does not exist."
    }
