from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_subraces(create_subrace, db_session):
    response = client.get("/api/subraces")
    assert response.status_code == 200
    assert response.json() == {
        "subraces": [
            {"name": "Duergar", "race_id": 1, "id": 1},
        ]
    }


def test_get_no_subraces(db_session):
    response = client.get("/api/subraces")
    assert response.status_code == 404
    assert response.json() == {"detail": "No subraces found."}


def test_get_subrace(create_subrace, db_session):
    response = client.get("/api/subraces/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Duergar",
        "race": {"id": 1, "name": "Dwarf"},
        "resistances": [],
    }


def test_get_no_subrace(create_subrace, db_session):
    response = client.get("/api/subraces/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_post_subrace(create_race, create_effect, db_session):
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
            "resistances": [1],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New subrace 'Locathah' has been added tot he database.",
        "subrace": {"id": 1, "name": "Locathah", "race_id": 1},
    }


def test_post_duplicate_subrace(create_race, create_effect, db_session):
    client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
            "resistances": [1],
        },
    )
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
            "resistances": [1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Subrace already exists."}


def test_post_subrace_wrong_race(create_race, create_effect, db_session):
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 2,
            "resistances": [1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The class you are trying to bind to this subrace does not exist."
    }


def test_post_subrace_wrong_effect(create_race, create_effect, db_session):
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
            "resistances": [2],
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The resistance you are trying to bind to this subrace does not exist."
    }
