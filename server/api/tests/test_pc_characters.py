from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_pc_characters(create_pc, db_session):
    response = client.get("/api/pc_characters")
    assert response.status_code == 200
    assert response.json() == {
        "pc_characters": [
            {
                "name": "Rhoetus",
                "size_id": 1,
                "description": "A centaur barbarian.",
                "alive": True,
                "creature": "pc_characters",
                "id": 1,
                "active": True,
                "armour_class": 17,
                "image": None,
                "race": 1,
                "user_id": 1,
                "information": "Some information about Rhoetus.",
                "subrace": 1,
                "type_id": 1,
            }
        ]
    }


def test_get_no_pc_characters(db_session):
    response = client.get("/api/pc_characters")
    assert response.status_code == 404
    assert response.json() == {"detail": "No PC characters found."}


def test_get_pc_character(create_pc, db_session):
    response = client.get("/api/pc_characters/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Rhoetus",
        "active": True,
        "alive": True,
        "armour_class": 17,
        "classes": [{"name": "Artificer", "id": 1}],
        "subclasses": [{"name": "Alchemist", "class_id": 1, "id": 1}],
        "race": 1,
        "subrace": 1,
        "creature_type": {"name": "Aberration", "id": 1},
        "description": "A centaur barbarian.",
        "information": "Some information about Rhoetus.",
        "size": {"name": "Tiny", "id": 1},
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
        "image": None,
        "user": {"name": "test", "password": None, "image": None, "id": 1},
        "parties": [{"name": "Murder Hobo Party", "id": 1}],
    }


def test_get_no_pc_character(create_pc, db_session):
    response = client.get("/api/pc_characters/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "PC character not found."}
