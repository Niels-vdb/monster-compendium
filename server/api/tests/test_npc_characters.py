from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_npc_characters(create_npc, db_session):
    response = client.get("/api/npc_characters")
    assert response.status_code == 200
    assert response.json() == {
        "npc_characters": [
            {
                "information": None,
                "subrace": None,
                "type_id": 1,
                "name": "Fersi (Oracle)",
                "size_id": 1,
                "description": None,
                "alive": True,
                "creature": "npc_characters",
                "active": True,
                "armour_class": None,
                "id": 1,
                "image": None,
                "race": None,
            }
        ]
    }


def test_get_no_npc_characters(db_session):
    response = client.get("/api/npc_characters")
    assert response.status_code == 404
    assert response.json() == {"detail": "No NPC characters found."}


def test_get_npc_character(create_npc, db_session):
    response = client.get("/api/npc_characters/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Fersi (Oracle)",
        "description": None,
        "information": None,
        "active": True,
        "alive": True,
        "armour_class": None,
        "image": None,
        "race": None,
        "subrace": None,
        "size": {"name": "Tiny", "id": 1},
        "type": 1,
        "creature_type": {"name": "Aberration", "id": 1},
        "parties": [],
        "classes": [],
        "subclasses": [],
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
    }


def test_get_no_npc_character(create_npc, db_session):
    response = client.get("/api/npc_characters/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "NPC character not found."}
