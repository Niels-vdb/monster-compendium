from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_races(create_race, db_session):
    response = client.get("/api/races")
    assert response.status_code == 200
    assert response.json() == {
        "races": [
            {"id": 1, "name": "Dwarf", "size_id": 1},
        ]
    }


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
        "subraces": [],
        "resistances": [],
    }


def test_get_no_race(create_race, db_session):
    response = client.get("/api/races/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}
