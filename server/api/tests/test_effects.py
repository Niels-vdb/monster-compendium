from fastapi.testclient import TestClient

from server.database.models.effects import Effect

from .conftest import app

client = TestClient(app)


def test_get_effects(create_effect, db_session):
    response = client.get("/api/effects")
    assert response.status_code == 200
    assert response.json() == {
        "effects": [
            {"id": 1, "name": "Fire"},
        ]
    }


def test_get_no_users(db_session):
    response = client.get("/api/effects")
    assert response.status_code == 404
    assert response.json() == {"detail": "No effects found."}


def test_get_effect(create_effect, db_session):
    response = client.get("/api/effects/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Fire"}


def test_get_no_effect(create_effect, db_session):
    response = client.get("/api/effects/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect not found."}


def test_post_effect(db_session):
    response = client.post(
        "/api/effects",
        json={
            "effect_name": "Fire",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New effect 'Fire' has been added to the database.",
        "effect": {"id": 1, "name": "Fire"},
    }


def test_post_duplicate_effect(db_session):
    client.post(
        "/api/effects",
        json={
            "effect_name": "Fire",
        },
    )
    response = client.post(
        "/api/effects",
        json={
            "effect_name": "Fire",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Effect already exists."}


def test_effect_name_put(create_effect, db_session):
    response = client.put(
        f"/api/effects/{create_effect.id}",
        json={"effect_name": "Slashing"},
    )
    effect = db_session.query(Effect).first()
    assert response.status_code == 200
    assert effect.name == "Slashing"
    assert response.json() == {
        "message": "Effect 'Slashing' has been updated.",
        "effect": {"id": 1, "name": "Slashing"},
    }


def test_effect_duplicate_name_put(create_effect, db_session):
    effect = Effect(name="Slashing")
    db_session.add(effect)
    db_session.commit()
    response = client.put(
        f"/api/effects/{effect.id}",
        json={"effect_name": "Fire"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_effect_fake_effect_put(create_race, create_effect, db_session):
    response = client.put(
        "/api/effects/2",
        json={"effect_name": "Slashing"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The effect you are trying to update does not exist.",
    }


def test_effect_delete(create_effect, db_session):
    response = client.delete(f"/api/effects/{create_effect.id}")
    effect = db_session.query(Effect).filter(Effect.id == create_effect.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": f"Effect has been deleted."}
    assert effect == None


def test_effect_fake_delete(create_effect, db_session):
    response = client.delete(f"/api/effects/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The effect you are trying to delete does not exist."
    }
