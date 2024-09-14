from fastapi.testclient import TestClient

from server.database.models.monsters import Monster

from .conftest import app


client = TestClient(app)


def test_get_monsters(create_monster, db_session):
    response = client.get("/api/monsters")
    assert response.status_code == 200
    assert response.json() == {
        "monsters": [
            {
                "information": "Some information about this big hippo, like his knowledge about firearms.",
                "subrace": None,
                "type_id": 1,
                "id": 1,
                "name": "Giff",
                "size_id": 1,
                "description": "A large hippo like creature",
                "alive": True,
                "creature": "monsters",
                "active": True,
                "armour_class": 16,
                "image": None,
                "race": None,
            }
        ]
    }


def test_get_no_monsters(db_session):
    response = client.get("/api/monsters")
    assert response.status_code == 404
    assert response.json() == {"detail": "No monsters found."}


def test_get_monster(create_monster, db_session):
    response = client.get("/api/monsters/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Giff",
        "description": "A large hippo like creature",
        "information": "Some information about this big hippo, like his knowledge about firearms.",
        "alive": True,
        "active": True,
        "armour_class": 16,
        "image": None,
        "race": None,
        "subrace": None,
        "size": {"id": 1, "name": "Tiny"},
        "creature_type": {"id": 1, "name": "Aberration"},
        "parties": [],
        "classes": [{"id": 1, "name": "Artificer"}],
        "subclasses": [{"class_id": 1, "name": "Alchemist", "id": 1}],
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
    }


def test_get_no_monster(create_monster, db_session):
    response = client.get("/api/monsters/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Monster not found."}


def test_post_monster(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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
        "message": "New monster 'Giff' has been added to the database.",
        "monster": {
            "id": 1,
            "name": "Giff",
            "size_id": 1,
            "description": " A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 22,
            "image": None,
            "race": 1,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": 1,
            "type_id": 1,
        },
    }


def test_post_monster_fake_class(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_subclass(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_race(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_subrace(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_size(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_type(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_party(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_resistance(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_immunity(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_post_monster_fake_vulnerabilities(
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
        "/api/monsters",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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


def test_monster_delete(create_monster, db_session):
    response = client.delete(f"/api/monsters/{create_monster.id}")
    monster = db_session.query(Monster).filter(Monster.id == create_monster.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": "Monster has been deleted."}
    assert monster == None


def test_monster_fake_delete(create_monster, db_session):
    response = client.delete(f"/api/monsters/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The monster you are trying to delete does not exist."
    }
