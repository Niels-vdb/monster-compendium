from fastapi.testclient import TestClient

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
        "message": "New effect 'Fire' has been added tot he database.",
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
