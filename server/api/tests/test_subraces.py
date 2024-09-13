from fastapi.testclient import TestClient

from server.database.models.races import Race, Subrace

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
        "message": "New subrace 'Locathah' has been added to the database.",
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
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to bind to this subrace does not exist."
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


def test_subrace_name_put(create_subrace, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        json={"subrace_name": "Hill"},
    )
    subrace = db_session.query(Subrace).first()
    assert response.status_code == 200
    assert subrace.name == "Hill"
    assert response.json() == {
        "message": "Subrace 'Hill' has been updated.",
        "subrace": {"race_id": 1, "name": "Hill", "id": 1},
    }


def test_subrace_race_put(create_subrace, create_size, db_session):
    new_race = Race(name="Halfling")
    db_session.add(new_race)
    db_session.commit()
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        json={"race_id": 2},
    )
    subrace = db_session.query(Subrace).first()

    assert response.status_code == 200
    assert subrace.race_id == 2
    assert response.json() == {
        "message": "Subrace 'Duergar' has been updated.",
        "subrace": {"name": "Duergar", "race_id": 2, "id": 1},
    }


def test_subrace_fake_race_put(create_race, create_subrace, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        json={"subrace_name": "Hill", "race_id": 2},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to link to this subrace does not exist.",
    }


def test_subrace_resistance_put(create_subrace, create_effect, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        json={"resistances": [1]},
    )
    subrace = db_session.query(Subrace).first()
    assert response.status_code == 200
    assert subrace.resistances[0].id == 1
    assert response.json() == {
        "message": "Subrace 'Duergar' has been updated.",
        "subrace": {"race_id": 1, "name": "Duergar", "id": 1},
    }


def test_subrace_fake_resistance_put(create_subrace, create_effect, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        json={"resistances": [2]},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The effect you are trying to link to this subrace does not exist.",
    }


def test_subrace_fake_subrace_put(create_race, create_subrace, db_session):
    response = client.put(
        "/api/subraces/2",
        json={"subrace_name": "Hill"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The subrace you are trying to update does not exist.",
    }


def test_subrace_delete(create_subrace, db_session):
    response = client.delete(f"/api/subraces/{create_subrace.id}")
    subrace = db_session.query(Subrace).filter(Subrace.id == create_subrace.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": f"Subrace has been deleted."}
    assert subrace == None


def test_subrace_delete(create_subrace, db_session):
    response = client.delete(f"/api/subraces/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The subrace you are trying to delete does not exist."
    }
