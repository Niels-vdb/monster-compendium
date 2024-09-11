from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_races(create_race, db_session):
    response = client.get("/api/races")

    assert response.status_code == 200
    assert response.json() == {"races": [{"id": 1, "name": "Dwarf"}]}


def test_get_no_races(db_session):
    response = client.get("/api/races")
    assert response.status_code == 404
    assert response.json() == {"detail": "No races found."}


def test_get_race(create_race, db_session):
    response = client.get("/api/races/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Dwarf",
        "sizes": [{"name": "Tiny", "id": 1}],
        "subraces": [],
        "resistances": [],
    }


def test_get_no_race(create_race, db_session):
    response = client.get("/api/races/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_post_race(create_size, create_effect, db_session):
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [1],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New race 'Locathah' has been added tot he database.",
        "race": {"name": "Locathah", "id": 1},
    }


def test_post_duplicate_race(create_size, create_effect, db_session):
    client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [1],
        },
    )
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Race already exists."}


def test_post_race_wrong_size(create_size, create_effect, db_session):
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [2],
            "resistances": [1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The size or resistance you are trying to bind to this race does not exist."
    }


def test_post_race_wrong_effect(create_size, create_effect, db_session):
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [2],
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The size or resistance you are trying to bind to this race does not exist."
    }
