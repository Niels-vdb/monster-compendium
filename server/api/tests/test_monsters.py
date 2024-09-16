from typing import Any
from fastapi.testclient import TestClient

from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.effects import Effect
from server.database.models.monsters import Monster
from server.database.models.users import Party

from .conftest import app


client = TestClient(app)


def test_get_monsters(create_monster, db_session):
    response = client.get("/api/monsters")
    assert response.status_code == 200
    assert response.json() == {
        "monsters": [
            {
                "name": "Giff",
                "race": None,
                "description": "A large hippo like creature",
                "alive": True,
                "subrace": None,
                "active": True,
                "type_id": 1,
                "id": 1,
                "armour_class": 16,
                "size_id": 1,
                "walking_speed": 30,
                "creature": "monsters",
                "swimming_speed": 20,
                "information": "Some information about this big hippo, like his knowledge about firearms.",
                "flying_speed": 0,
                "image": None,
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
        "walking_speed": 30,
        "swimming_speed": 20,
        "flying_speed": 0,
        "image": None,
        "race": None,
        "subrace": None,
        "size": {"id": 1, "name": "Tiny"},
        "creature_type": {"name": "Aberration", "id": 1},
        "parties": [{"name": "Murder Hobo Party", "id": 1}],
        "classes": [{"id": 1, "name": "Artificer"}],
        "subclasses": [{"name": "Alchemist", "class_id": 1, "id": 1}],
        "resistances": [{"id": 1, "name": "Fire"}],
        "immunities": [{"id": 1, "name": "Fire"}],
        "vulnerabilities": [{"id": 1, "name": "Fire"}],
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
            "walking_speed": 35,
            "classes": [1],
            "subclasses": [1],
            "race": 1,
            "subrace": 1,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [{"effect_id": 1, "condition": "When in rage"}],
            "immunities": [{"effect_id": 1, "condition": "When in rage"}],
            "vulnerabilities": [{"effect_id": 1, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New monster 'Giff' has been added to the database.",
        "monster": {
            "name": "Giff",
            "race": 1,
            "description": " A large hippo like creature",
            "alive": True,
            "subrace": 1,
            "active": True,
            "type_id": 1,
            "id": 1,
            "armour_class": 22,
            "size_id": 1,
            "walking_speed": 35,
            "creature": "monsters",
            "swimming_speed": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "flying_speed": None,
            "image": None,
        },
    }


def test_post_monster_fake_class(
    create_class,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "classes": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Class with this id does not exist."}


def test_post_monster_fake_subclass(
    create_subclass,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "subclasses": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass with this id does not exist."}


def test_post_monster_fake_race(
    create_race,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "race": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Race with this id does not exist."}


def test_post_monster_fake_subrace(
    create_subrace,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "race": 1,
            "subrace": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace with this id does not exist."}


def test_post_monster_fake_size(
    create_size,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "size_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Size with this id does not exist."}


def test_post_monster_fake_type(
    create_type,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "type_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Type with this id does not exist."}


def test_post_monster_fake_party(
    create_party,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "parties": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Party with this id does not exist."}


def test_post_monster_fake_resistance(
    create_effect,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "resistances": [{"effect_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_post_monster_fake_immunity(
    create_effect,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "immunities": [{"effect_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_post_monster_fake_vulnerabilities(
    create_effect,
    db_session,
):
    response = client.post(
        "/api/monsters",
        json={
            "name": "Giff",
            "vulnerabilities": [{"effect_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_monster_add_put(
    create_monster,
    create_race,
    create_subrace,
    create_class,
    create_subclass,
    db_session,
):

    race_id = create_race.id
    subrace_id = create_subrace.id

    size = Size(name="Medium")
    db_session.add(size)

    new_type = Type(name="Celestial")
    db_session.add(new_type)

    new_class = Class(name="Barbarian")
    db_session.add(new_class)

    new_subclass = Subclass(name="Armourer")
    db_session.add(new_subclass)

    new_party = Party(name="Hobo Helping Party")
    db_session.add(new_party)

    new_resistance = Effect(name="Slashing")
    db_session.add(new_resistance)

    db_session.commit()

    size_id = size.id
    type_id = new_type.id
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={
            "name": "Froghemoth",
            "information": "Some new information about Froghemoth.",
            "description": "Something else about the Froghemoth.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 40,
            "swimming_speed": 40,
            "flying_speed": 5,
            "race": race_id,
            "subrace": subrace_id,
            "size_id": size_id,
            "type_id": type_id,
            "classes": [2],
            "add_class": True,
            "subclasses": [2],
            "add_subclass": True,
            "parties": [2],
            "add_parties": True,
            "resistances": [
                {
                    "effect_id": 2,
                    "condition": "When in rage",
                    "add_effect": True,
                }
            ],
            "immunities": [
                {
                    "effect_id": 2,
                    "condition": "When in rage",
                    "add_effect": True,
                }
            ],
            "vulnerabilities": [
                {
                    "effect_id": 2,
                    "condition": "When in rage",
                    "add_effect": True,
                }
            ],
        },
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.name == "Froghemoth"
    assert monster.information == "Some new information about Froghemoth."
    assert monster.description == "Something else about the Froghemoth."
    assert monster.alive == False
    assert monster.active == False
    assert monster.armour_class == 20
    assert monster.walking_speed == 40
    assert monster.swimming_speed == 40
    assert monster.flying_speed == 5
    assert monster.race == race_id
    assert monster.subrace == subrace_id
    assert monster.size_id == size_id
    assert monster.type_id == type_id
    assert len(monster.classes) == 2
    assert len(monster.subclasses) == 2
    assert len(monster.parties) == 2
    assert len(monster.immunities) == 2
    assert len(monster.resistances) == 2
    assert len(monster.vulnerabilities) == 2
    assert response.json() == {
        "message": "Monster 'Froghemoth' has been updated.",
        "monster": {
            "name": "Froghemoth",
            "race": 1,
            "subrace": 1,
            "description": "Something else about the Froghemoth.",
            "alive": False,
            "type_id": 2,
            "active": False,
            "id": 1,
            "size_id": 2,
            "armour_class": 20,
            "creature": "monsters",
            "walking_speed": 40,
            "swimming_speed": 40,
            "flying_speed": 5,
            "information": "Some new information about Froghemoth.",
            "image": None,
        },
    }


def test_monster_remove_put(
    create_monster,
    create_race,
    create_subrace,
    db_session,
):
    race_id = create_race.id
    subrace_id = create_subrace.id

    size = Size(name="Medium")
    db_session.add(size)

    new_type = Type(name="Celestial")
    db_session.add(new_type)

    db_session.commit()

    size_id = size.id
    type_id = new_type.id
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={
            "name": "Froghemoth",
            "information": "Some new information about Froghemoth.",
            "description": "Something else about the Froghemoth.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "race": race_id,
            "subrace": subrace_id,
            "size_id": size_id,
            "type_id": type_id,
            "classes": [1],
            "add_class": False,
            "subclasses": [1],
            "add_subclass": False,
            "parties": [1],
            "add_parties": False,
            "resistances": [
                {
                    "effect_id": 1,
                    "add_effect": False,
                }
            ],
            "immunities": [
                {
                    "effect_id": 1,
                    "add_effect": False,
                }
            ],
            "vulnerabilities": [
                {
                    "effect_id": 1,
                    "add_effect": False,
                }
            ],
        },
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.name == "Froghemoth"
    assert monster.information == "Some new information about Froghemoth."
    assert monster.description == "Something else about the Froghemoth."
    assert monster.alive == False
    assert monster.active == False
    assert monster.armour_class == 20
    assert monster.walking_speed == 35
    assert monster.swimming_speed == 30
    assert monster.flying_speed == 5
    assert monster.race == race_id
    assert monster.subrace == subrace_id
    assert monster.size_id == size_id
    assert monster.type_id == type_id
    assert len(monster.classes) == 0
    assert len(monster.subclasses) == 0
    assert len(monster.parties) == 0
    assert len(monster.immunities) == 0
    assert len(monster.resistances) == 0
    assert len(monster.vulnerabilities) == 0
    assert response.json() == {
        "message": "Monster 'Froghemoth' has been updated.",
        "monster": {
            "type_id": 2,
            "name": "Froghemoth",
            "size_id": 2,
            "description": "Something else about the Froghemoth.",
            "id": 1,
            "alive": False,
            "creature": "monsters",
            "active": False,
            "armour_class": 20,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "image": None,
            "information": "Some new information about Froghemoth.",
            "race": 1,
            "subrace": 1,
        },
    }


def test_monster_fake_race_put(create_monster, db_session):
    response = client.put(f"/api/monsters/{create_monster.id}", json={"race": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Race with this id does not exist."}


def test_monster_fake_subrace_put(create_monster, db_session):
    response = client.put(f"/api/monsters/{create_monster.id}", json={"subrace": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace with this id does not exist."}


def test_monster_fake_size_put(create_monster, db_session):
    response = client.put(f"/api/monsters/{create_monster.id}", json={"size_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Size with this id does not exist."}


def test_monster_fake_type_put(create_monster, db_session):
    response = client.put(f"/api/monsters/{create_monster.id}", json={"type_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Type with this id does not exist."}


def test_monster_fake_class_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"classes": [3], "add_classes": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Class with this id does not exist."}


def test_monster_fake_subclass_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"subclasses": [3], "add_subclasses": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass with this id does not exist."}


def test_monster_fake_part_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"parties": [3], "add_parties": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Party with this id does not exist."}


def test_monster_fake_resistance_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={
            "resistances": [
                {
                    "effect_id": 3,
                    "add_effect": False,
                }
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_monster_fake_vulnerability_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={
            "vulnerabilities": [
                {
                    "effect_id": 3,
                    "add_effect": False,
                }
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_monster_fake_immunity_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={
            "immunities": [
                {
                    "effect_id": 3,
                    "add_effect": False,
                }
            ],
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
