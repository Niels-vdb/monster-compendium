from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_npc_characters(create_npc, db_session):
    response = client.get("/api/non_player_characters")
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
    response = client.get("/api/non_player_characters")
    assert response.status_code == 404
    assert response.json() == {"detail": "No NPC characters found."}


def test_get_npc_character(create_npc, db_session):
    response = client.get("/api/non_player_characters/1")
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
    response = client.get("/api/non_player_characters/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "NPC character not found."}


def test_post_npc(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "classes": [1],
            "subclasses": [1],
            "race": 1,
            "subrace": 1,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New npc 'Volothamp Geddarm' has been added to the database.",
        "npc_character": {
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "subrace": 1,
            "type_id": 1,
            "name": "Volothamp Geddarm",
            "size_id": 1,
            "description": " Volo for short",
            "alive": True,
            "creature": "npc_characters",
            "active": True,
            "armour_class": 22,
            "id": 1,
            "image": None,
            "race": 1,
        },
    }


def test_post_npc_fake_class(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "classes": [2],
            "subclasses": [1],
            "race": 1,
            "subrace": 1,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Class with this id does not exist."}


def test_post_npc_fake_subclass(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "classes": [1],
            "subclasses": [2],
            "race": 1,
            "subrace": 1,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass with this id does not exist."}


def test_post_npc_fake_race(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "classes": [1],
            "subclasses": [1],
            "race": 2,
            "subrace": 1,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Race with this id does not exist."}


def test_post_npc_fake_subrace(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "classes": [1],
            "subclasses": [1],
            "race": 1,
            "subrace": 2,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace with this id does not exist."}


def test_post_npc_fake_size(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "size_id": 2,
            "type_id": 1,
            "parties": [1],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Size with this id does not exist."}


def test_post_npc_fake_type(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "size_id": 1,
            "type_id": 2,
            "parties": [1],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Type with this id does not exist."}


def test_post_npc_fake_party(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "size_id": 1,
            "type_id": 1,
            "parties": [2],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Party with this id does not exist."}


def test_post_npc_fake_resistance(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [2],
            "immunities": [1],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_post_npc_fake_immunity(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [1],
            "immunities": [2],
            "vulnerabilities": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_post_npc_fake_vulnerabilities(
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_effect,
    db_session,
):
    response = client.post(
        "/api/non_player_characters",
        json={
            "name": "Volothamp Geddarm",
            "description": " Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [1],
            "immunities": [1],
            "vulnerabilities": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}
