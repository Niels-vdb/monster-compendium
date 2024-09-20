from fastapi.testclient import TestClient

from server.database.models.races import Race
from server.database.models.subraces import Subrace

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
        "immunities": [],
        "vulnerabilities": [],
        "advantages": [],
        "disadvantages": [],
    }


def test_get_no_subrace(create_subrace, db_session):
    response = client.get("/api/subraces/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_post_subrace(create_subrace, create_damage_type, create_attribute, db_session):
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
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
        "message": "New subrace 'Locathah' has been added to the database.",
        "subrace": {"race_id": 1, "id": 2, "name": "Locathah"},
    }


def test_post_duplicate_subrace(create_subrace, db_session):
    client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
        },
    )
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Subrace already exists."}


def test_post_subrace_wrong_subrace(create_subrace, db_session):
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to bind to this subrace does not exist."
    }


def test_post_subrace_wrong_damage_type(create_subrace, create_damage_type, db_session):
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
            "resistances": [
                {"damage_type_id": 2, "condition": "When in rage"},
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with id '2' does not exist."}


def test_post_subrace_wrong_attribute(create_subrace, create_attribute, db_session):
    response = client.post(
        "/api/subraces",
        json={
            "subrace_name": "Locathah",
            "race_id": 1,
            "advantages": [
                {"attribute_id": 2, "condition": "When in rage"},
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute with id '2' does not exist."}


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


def test_subrace_duplicate_name_put(create_subrace, create_race, db_session):
    subrace = Subrace(name="Hill", race_id=1)
    db_session.add(subrace)
    db_session.commit()
    response = client.put(
        f"/api/subraces/{subrace.id}",
        json={"subrace_name": "Duergar"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_subrace_race_put(create_subrace, create_race, create_size, db_session):
    new_race = Race(name="Halfling", sizes=[create_size])
    db_session.add(new_race)
    db_session.commit()
    db_session.refresh(new_race)
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        json={"race_id": new_race.id},
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


def test_subrace_resistance_put(create_subrace, create_damage_type, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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
    subrace = db_session.query(Subrace).first()
    assert response.status_code == 200
    assert len(subrace.resistances) == 1
    assert response.json() == {
        "message": "Subrace 'Duergar' has been updated.",
        "subrace": {"id": 1, "name": "Duergar", "race_id": 1},
    }


def test_subrace_fake_resistance_put(create_subrace, create_damage_type, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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


def test_subrace_vulnerability_put(create_subrace, create_damage_type, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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
    subrace = db_session.query(Subrace).first()
    assert response.status_code == 200
    assert len(subrace.vulnerabilities) == 1
    assert response.json() == {
        "message": "Subrace 'Duergar' has been updated.",
        "subrace": {"id": 1, "name": "Duergar", "race_id": 1},
    }


def test_subrace_fake_vulnerability_put(create_subrace, create_damage_type, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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


def test_subrace_immunity_put(create_subrace, create_damage_type, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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
    subrace = db_session.query(Subrace).first()
    assert response.status_code == 200
    assert len(subrace.immunities) == 1
    assert response.json() == {
        "message": "Subrace 'Duergar' has been updated.",
        "subrace": {"id": 1, "name": "Duergar", "race_id": 1},
    }


def test_subrace_fake_immunity_put(create_subrace, create_damage_type, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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


def test_subrace_advantage_put(create_subrace, create_attribute, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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
    subrace = db_session.query(Subrace).first()
    assert response.status_code == 200
    assert len(subrace.advantages) == 1
    assert response.json() == {
        "message": "Subrace 'Duergar' has been updated.",
        "subrace": {"id": 1, "name": "Duergar", "race_id": 1},
    }


def test_subrace_fake_advantage_put(create_subrace, create_attribute, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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


def test_subrace_disadvantage_put(create_subrace, create_attribute, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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
    subrace = db_session.query(Subrace).first()
    assert response.status_code == 200
    assert len(subrace.disadvantages) == 1
    assert response.json() == {
        "message": "Subrace 'Duergar' has been updated.",
        "subrace": {"id": 1, "name": "Duergar", "race_id": 1},
    }


def test_subrace_fake_disadvantage_put(create_subrace, create_attribute, db_session):
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
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


def test_subrace_fake_delete(create_subrace, db_session):
    response = client.delete(f"/api/subraces/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The subrace you are trying to delete does not exist."
    }
