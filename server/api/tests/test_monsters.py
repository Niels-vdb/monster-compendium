from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_monsters(create_monster, db_session):
    response = client.get("/api/monsters")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "monsters": [
            {
                "name": "Giff",
                "size_id": 1,
                "description": "A large hippo like creature",
                "alive": True,
                "creature": "monsters",
                "active": True,
                "armour_class": 16,
                "image": None,
                "id": 1,
                "race": None,
                "information": "Some information about this big hippo, like his knowledge about firearms.",
                "subrace": None,
                "type_id": 1,
            }
        ]
    }


def test_get_no_monsters(db_session):
    response = client.get("/api/monsters")
    assert response.status_code == 404
    assert response.json() == {"detail": "No monsters found."}


def test_get_monster(create_monster, db_session):
    response = client.get("/api/monsters/1")
    print(response.json())

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Giff",
        "active": True,
        "alive": True,
        "armour_class": 16,
        "classes": [{"name": "Artificer", "id": 1}],
        "subclasses": [{"name": "Alchemist", "class_id": 1, "id": 1}],
        "race": None,
        "subrace": None,
        "creature_type": {"name": "Aberration", "id": 1},
        "description": "A large hippo like creature",
        "information": "Some information about this big hippo, like his knowledge about firearms.",
        "size": {"name": "Tiny", "id": 1},
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
        "image": None,
    }


def test_get_no_monster(create_monster, db_session):
    response = client.get("/api/monsters/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Monster not found."}
