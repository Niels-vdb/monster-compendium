from fastapi.testclient import TestClient

from server.database.models.races import Race

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
        "message": "New race 'Locathah' has been added to the database.",
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


def test_race_name_put(create_race, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={"race_name": "Elf"},
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert race.name == "Elf"
    assert response.json() == {
        "message": "Subrace 'Elf' has been updated.",
        "subrace": {"id": 1, "name": "Elf"},
    }


def test_race_resistance_put(create_race, create_effect, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={"resistances": [1]},
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert race.resistances[0].id == 1
    assert response.json() == {
        "message": "Subrace 'Dwarf' has been updated.",
        "subrace": {"id": 1, "name": "Dwarf"},
    }


def test_race_fake_resistance_put(create_race, create_effect, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={"resistances": [2]},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The effect you are trying to link to this subrace does not exist."
    }


def test_race_size_put(create_race, create_effect, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={"sizes": [1]},
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert race.sizes[0].id == 1
    assert response.json() == {
        "message": "Subrace 'Dwarf' has been updated.",
        "subrace": {"id": 1, "name": "Dwarf"},
    }


def test_race_fake_size_put(create_race, create_effect, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={"sizes": [2]},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The size you are trying to link to this subrace does not exist."
    }


def test_fake_race_put(create_race, db_session):
    response = client.put(
        "/api/races/2",
        json={"race_name": "Elf"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to update does not exist.",
    }


def test_race_delete(create_race, db_session):
    response = client.delete(f"/api/races/{create_race.id}")
    race = db_session.query(Race).filter(Race.id == create_race.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": "Race has been deleted."}
    assert race == None


def test_race_fake_delete(create_race, db_session):
    response = client.delete(f"/api/races/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to delete does not exist."
    }
