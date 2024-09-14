from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_pc_characters(create_pc, db_session):
    response = client.get("/api/player_characters")
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
    response = client.get("/api/player_characters")
    assert response.status_code == 404
    assert response.json() == {"detail": "No PC characters found."}


def test_get_pc_character(create_pc, db_session):
    response = client.get("/api/player_characters/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Rhoetus",
        "description": "A centaur barbarian.",
        "information": "Some information about Rhoetus.",
        "alive": True,
        "active": True,
        "armour_class": 17,
        "image": None,
        "race": 1,
        "subrace": 1,
        "size": {"name": "Tiny", "id": 1},
        "creature_type": {"name": "Aberration", "id": 1},
        "user": {
            "password": None,
            "id": 1,
            "image": None,
            "username": "Test",
            "name": "test",
        },
        "parties": [{"id": 1, "name": "Murder Hobo Party"}],
        "classes": [{"name": "Artificer", "id": 1}],
        "subclasses": [{"id": 1, "class_id": 1, "name": "Alchemist"}],
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
    }


def test_get_no_pc_character(create_pc, db_session):
    response = client.get("/api/player_characters/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "PC character not found."}


def test_post_pc(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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
        "message": "New pc 'Gobby' has been added to the database.",
        "pc_character": {
            "information": "This guy reeeealy loves gemstones.",
            "subrace": 1,
            "type_id": 1,
            "name": "Gobby",
            "size_id": 1,
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "alive": True,
            "creature": "pc_characters",
            "active": True,
            "armour_class": 22,
            "image": None,
            "id": 1,
            "race": 1,
        },
    }


def test_post_pc_fake_class(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_subclass(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_race(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_subrace(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_size(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_type(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_party(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_resistance(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_immunity(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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


def test_post_pc_fake_vulnerabilities(
    create_user,
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
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obssed goblin.",
            "information": "This guy reeeealy loves gemstones.",
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
