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
        "sizes": [{"id": 1, "name": "Tiny"}],
        "subraces": [],
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
        "advantages": [],
        "disadvantages": [],
    }


def test_get_no_race(create_race, db_session):
    response = client.get("/api/races/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_post_race(create_size, create_damage_type, create_attribute, db_session):
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [
                {"damage_type_id": 1, "condition": "When in rage"},
            ],
            "immunities": [
                {"damage_type_id": 1, "condition": "When not in rage"},
            ],
            "vulnerabilities": [
                {"damage_type_id": 1, "condition": "When wearing armour"},
            ],
            "advantages": [
                {"attribute_id": 1, "condition": "When wearing a shield"},
            ],
            "disadvantages": [
                {"attribute_id": 1, "condition": "When not wearing a shield"},
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New race 'Locathah' has been added to the database.",
        "race": {
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [{"damage_type_id": 1, "condition": "When in rage"}],
            "immunities": [{"damage_type_id": 1, "condition": "When not in rage"}],
            "vulnerabilities": [
                {"damage_type_id": 1, "condition": "When wearing armour"}
            ],
            "advantages": [{"attribute_id": 1, "condition": "When wearing a shield"}],
            "disadvantages": [
                {"attribute_id": 1, "condition": "When not wearing a shield"}
            ],
        },
    }


def test_post_duplicate_race(create_size, db_session):
    client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
        },
    )
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Race already exists."}


def test_post_race_wrong_size(create_size, db_session):
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [2],
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The size you are trying to bind to this race does not exist."
    }


def test_post_race_wrong_damage_type(create_size, create_damage_type, db_session):
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [
                {"damage_type_id": 2, "condition": "When in rage"},
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with id '2' does not exist."}


def test_post_race_wrong_attribute(create_size, create_attribute, db_session):
    response = client.post(
        "/api/races",
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "advantages": [
                {"attribute_id": 2, "condition": "When in rage"},
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute with id '2' does not exist."}


def test_race_name_put(create_race, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={"race_name": "Elf"},
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert race.name == "Elf"
    assert response.json() == {
        "message": "Race 'Elf' has been updated.",
        "subrace": {"id": 1, "name": "Elf"},
    }


def test_race_duplicate_name_put(create_size, create_race, db_session):
    race = Race(name="Elf", sizes=[create_size])
    db_session.add(race)
    db_session.commit()
    response = client.put(
        f"/api/races/{race.id}",
        json={"race_name": "Dwarf"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_race_resistance_put(create_race, create_damage_type, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "resistances": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert len(race.resistances) == 1
    assert response.json() == {
        "message": "Race 'Dwarf' has been updated.",
        "subrace": {"id": 1, "name": "Dwarf"},
    }


def test_race_fake_resistance_put(create_race, create_damage_type, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "resistances": [
                {
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_race_vulnerability_put(create_race, create_damage_type, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "vulnerabilities": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert len(race.vulnerabilities) == 1
    assert response.json() == {
        "message": "Race 'Dwarf' has been updated.",
        "subrace": {"id": 1, "name": "Dwarf"},
    }


def test_race_fake_vulnerability_put(create_race, create_damage_type, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "vulnerabilities": [
                {
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_race_immunity_put(create_race, create_damage_type, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "immunities": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert len(race.immunities) == 1
    assert response.json() == {
        "message": "Race 'Dwarf' has been updated.",
        "subrace": {"id": 1, "name": "Dwarf"},
    }


def test_race_fake_immunity_put(create_race, create_damage_type, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "immunities": [
                {
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_race_advantage_put(create_race, create_attribute, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "advantages": [
                {
                    "attribute_id": 1,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ]
        },
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert len(race.advantages) == 1
    assert response.json() == {
        "message": "Race 'Dwarf' has been updated.",
        "subrace": {"id": 1, "name": "Dwarf"},
    }


def test_race_fake_advantage_put(create_race, create_attribute, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "advantages": [
                {
                    "attribute_id": 2,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ]
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_race_disadvantage_put(create_race, create_attribute, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "disadvantages": [
                {
                    "attribute_id": 1,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ]
        },
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert len(race.disadvantages) == 1
    assert response.json() == {
        "message": "Race 'Dwarf' has been updated.",
        "subrace": {"id": 1, "name": "Dwarf"},
    }


def test_race_fake_disadvantage_put(create_race, create_attribute, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={
            "disadvantages": [
                {
                    "attribute_id": 2,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ]
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_race_size_put(create_race, db_session):
    response = client.put(
        f"/api/races/{create_race.id}",
        json={"sizes": [1]},
    )
    race = db_session.query(Race).first()
    assert response.status_code == 200
    assert race.sizes[0].id == 1
    assert response.json() == {
        "message": "Race 'Dwarf' has been updated.",
        "subrace": {"id": 1, "name": "Dwarf"},
    }


def test_race_fake_size_put(create_race, db_session):
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
