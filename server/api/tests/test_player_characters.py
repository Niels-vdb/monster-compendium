from fastapi.testclient import TestClient

from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.damage_types import DamageType
from server.database.models.attributes import Attribute
from server.database.models.player_characters import PlayerCharacter
from server.database.models.users import Party

from .conftest import app


client = TestClient(app)


def test_get_pcs(create_pc, db_session):
    response = client.get("/api/player_characters")
    assert response.status_code == 200
    assert response.json() == {
        "player_characters": [
            {
                "name": "Rhoetus",
                "image": None,
                "user_id": 1,
                "description": "A centaur barbarian.",
                "alive": True,
                "race": 1,
                "active": True,
                "subrace": 1,
                "armour_class": 17,
                "type_id": 1,
                "walking_speed": 40,
                "size_id": 1,
                "id": 1,
                "swimming_speed": 10,
                "creature": "player_characters",
                "information": "Some information about Rhoetus.",
                "flying_speed": 0,
                "climbing_speed": None,
            }
        ]
    }


def test_get_no_pcs(db_session):
    response = client.get("/api/player_characters")
    assert response.status_code == 404
    assert response.json() == {"detail": "No player characters found."}


def test_get_pc(create_pc, db_session):
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
        "walking_speed": 40,
        "swimming_speed": 10,
        "flying_speed": 0,
        "climbing_speed": None,
        "image": None,
        "race": 1,
        "subrace": 1,
        "size": {"id": 1, "name": "Tiny"},
        "creature_type": {"id": 1, "name": "Aberration"},
        "user": {
            "name": "test",
            "image": None,
            "username": "Test",
            "password": None,
            "id": 1,
        },
        "parties": [{"name": "Murder Hobo Party", "id": 1}],
        "classes": [{"name": "Artificer", "id": 1}],
        "subclasses": [{"id": 1, "name": "Alchemist", "class_id": 1}],
        "resistances": [{"id": 1, "name": "Fire"}],
        "immunities": [{"id": 1, "name": "Fire"}],
        "vulnerabilities": [{"id": 1, "name": "Fire"}],
        "advantages": [{"name": "Charmed", "id": 1}],
        "disadvantages": [{"name": "Charmed", "id": 1}],
    }


def test_get_no_pc(create_pc, db_session):
    response = client.get("/api/player_characters/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Player character not found."}


def test_post_pc(
    create_user,
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_party,
    create_damage_type,
    create_attribute,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "description": "A gemstone obsessed goblin.",
            "information": "This guy reeeealy loves finding and sharing gemstones.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "climbing_speed": 5,
            "classes": [1],
            "subclasses": [1],
            "race": 1,
            "subrace": 1,
            "size_id": 1,
            "type_id": 1,
            "parties": [1],
            "resistances": [{"damage_type_id": 1, "condition": "When in rage"}],
            "immunities": [{"damage_type_id": 1, "condition": "When in rage"}],
            "vulnerabilities": [{"damage_type_id": 1, "condition": "When in rage"}],
            "advantages": [{"attribute_id": 1, "condition": "When in rage"}],
            "disadvantages": [{"attribute_id": 1, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New player character 'Gobby' has been added to the database.",
        "player_character": {
            "name": "Gobby",
            "user_id": 1,
            "image": None,
            "description": "A gemstone obsessed goblin.",
            "alive": True,
            "race": 1,
            "active": True,
            "subrace": 1,
            "type_id": 1,
            "armour_class": 22,
            "size_id": 1,
            "walking_speed": 35,
            "id": 1,
            "creature": "player_characters",
            "swimming_speed": 30,
            "flying_speed": 5,
            "information": "This guy reeeealy loves finding and sharing gemstones.",
            "climbing_speed": 5,
        },
    }


def test_post_pc_fake_class(
    create_user,
    create_class,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "classes": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This class does not exist."}


def test_post_pc_fake_subclass(
    create_user,
    create_subclass,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "subclasses": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This subclass does not exist."}


def test_post_pc_fake_race(
    create_user,
    create_race,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "race": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This race does not exist."}


def test_post_pc_fake_subrace(
    create_user,
    create_race,
    create_subrace,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "race": 1,
            "subrace": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This subrace does not exist."}


def test_post_pc_fake_size(
    create_user,
    create_size,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "size_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This size does not exist."}


def test_post_pc_fake_type(
    create_user,
    create_type,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "type_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This type does not exist."}


def test_post_pc_fake_party(
    create_user,
    create_party,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "parties": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This party does not exist."}


def test_post_pc_fake_resistance(
    create_user,
    create_damage_type,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "resistances": [{"damage_type_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This damage type does not exist."}


def test_post_pc_fake_immunity(
    create_user,
    create_damage_type,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "immunities": [{"damage_type_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This damage type does not exist."}


def test_post_pc_fake_vulnerabilities(
    create_user,
    create_damage_type,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "vulnerabilities": [{"damage_type_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This damage type does not exist."}


def test_post_pc_fake_advantages(
    create_user,
    create_attribute,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "advantages": [{"attribute_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This attribute does not exist."}


def test_post_pc_fake_disadvantages(
    create_user,
    create_attribute,
    db_session,
):
    response = client.post(
        "/api/player_characters",
        json={
            "name": "Gobby",
            "user_id": 1,
            "disadvantages": [{"attribute_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This attribute does not exist."}


def test_pc_add_put(
    create_pc,
    create_race,
    create_subrace,
    create_class,
    create_subclass,
    create_damage_type,
    create_attribute,
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

    new_resistance = DamageType(name="Slashing")
    db_session.add(new_resistance)

    new_attribute = Attribute(name="Poisoned")
    db_session.add(new_attribute)

    db_session.commit()

    size_id = size.id
    type_id = new_type.id

    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={
            "name": "Electra",
            "information": "Some new information about Electra.",
            "description": "Something else about the Electra.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "climbing_speed": 5,
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
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ],
            "immunities": [
                {
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ],
            "vulnerabilities": [
                {
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ],
            "advantages": [
                {
                    "attribute_id": 2,
                    "add_attribute": True,
                    "condition": "When wearing armour",
                }
            ],
            "disadvantages": [
                {
                    "attribute_id": 2,
                    "add_attribute": True,
                    "condition": "When not wearing armour",
                }
            ],
        },
    )
    pc = db_session.query(PlayerCharacter).first()
    assert response.status_code == 200
    assert pc.name == "Electra"
    assert pc.information == "Some new information about Electra."
    assert pc.description == "Something else about the Electra."
    assert pc.alive == False
    assert pc.active == False
    assert pc.armour_class == 20
    assert pc.walking_speed == 35
    assert pc.swimming_speed == 30
    assert pc.flying_speed == 5
    assert pc.race == race_id
    assert pc.subrace == subrace_id
    assert pc.size_id == size_id
    assert pc.type_id == type_id
    assert len(pc.classes) == 2
    assert len(pc.subclasses) == 2
    assert len(pc.parties) == 2
    assert len(pc.immunities) == 2
    assert len(pc.resistances) == 2
    assert len(pc.vulnerabilities) == 2
    assert len(pc.advantages) == 2
    assert len(pc.disadvantages) == 2
    assert response.json() == {
        "message": "Player character 'Electra' has been updated.",
        "player_character": {
            "name": "Electra",
            "user_id": 1,
            "image": None,
            "description": "Something else about the Electra.",
            "alive": False,
            "race": 1,
            "active": False,
            "subrace": 1,
            "type_id": 2,
            "armour_class": 20,
            "size_id": 2,
            "walking_speed": 35,
            "id": 1,
            "creature": "player_characters",
            "swimming_speed": 30,
            "flying_speed": 5,
            "information": "Some new information about Electra.",
            "climbing_speed": 5,
        },
    }


def test_pc_remove_put(
    create_pc,
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

    db_session.commit()

    size_id = size.id
    type_id = new_type.id

    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={
            "name": "Electra",
            "information": "Some new information about Electra.",
            "description": "Something else about the Electra.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "climbing_speed": 5,
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
                    "damage_type_id": 1,
                    "add_damage_type": False,
                }
            ],
            "immunities": [
                {
                    "damage_type_id": 1,
                    "add_damage_type": False,
                }
            ],
            "vulnerabilities": [
                {
                    "damage_type_id": 1,
                    "add_damage_type": False,
                }
            ],
            "advantages": [
                {
                    "attribute_id": 1,
                    "add_attribute": False,
                }
            ],
            "disadvantages": [
                {
                    "attribute_id": 1,
                    "add_attribute": False,
                }
            ],
        },
    )

    pc = db_session.query(PlayerCharacter).first()
    assert response.status_code == 200
    assert pc.name == "Electra"
    assert pc.information == "Some new information about Electra."
    assert pc.description == "Something else about the Electra."
    assert pc.alive == False
    assert pc.active == False
    assert pc.armour_class == 20
    assert pc.walking_speed == 35
    assert pc.swimming_speed == 30
    assert pc.flying_speed == 5
    assert pc.race == race_id
    assert pc.subrace == subrace_id
    assert pc.size_id == size_id
    assert pc.type_id == type_id
    assert len(pc.classes) == 0
    assert len(pc.subclasses) == 0
    assert len(pc.parties) == 0
    assert len(pc.immunities) == 0
    assert len(pc.resistances) == 0
    assert len(pc.vulnerabilities) == 0
    assert len(pc.advantages) == 0
    assert len(pc.disadvantages) == 0
    assert response.json() == {
        "message": "Player character 'Electra' has been updated.",
        "player_character": {
            "name": "Electra",
            "user_id": 1,
            "image": None,
            "description": "Something else about the Electra.",
            "alive": False,
            "race": 1,
            "active": False,
            "subrace": 1,
            "type_id": 2,
            "armour_class": 20,
            "size_id": 2,
            "walking_speed": 35,
            "id": 1,
            "creature": "player_characters",
            "swimming_speed": 30,
            "flying_speed": 5,
            "information": "Some new information about Electra.",
            "climbing_speed": 5,
        },
    }


def test_pc_fake_race_put(create_pc, db_session):
    response = client.put(f"/api/player_characters/{create_pc.id}", json={"race": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "This race does not exist."}


def test_pc_fake_subrace_put(create_pc, db_session):
    response = client.put(f"/api/player_characters/{create_pc.id}", json={"subrace": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "This subrace does not exist."}


def test_pc_fake_size_put(create_pc, db_session):
    response = client.put(f"/api/player_characters/{create_pc.id}", json={"size_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "This size does not exist."}


def test_pc_fake_type_put(create_pc, db_session):
    response = client.put(f"/api/player_characters/{create_pc.id}", json={"type_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "This type does not exist."}


def test_pc_fake_class_put(create_pc, db_session):
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={"classes": [3], "add_classes": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This class does not exist."}


def test_pc_fake_subclass_put(create_pc, db_session):
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={"subclasses": [3], "add_subclasses": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This subclass does not exist."}


def test_pc_fake_party_put(create_pc, db_session):
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={"parties": [3], "add_parties": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This party does not exist."}


def test_pc_fake_resistance_put(create_pc, db_session):
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={
            "resistances": [
                {
                    "damage_type_id": 3,
                    "add_damage_type": False,
                }
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This damage type does not exist."}


def test_pc_fake_vulnerability_put(create_pc, db_session):
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={
            "vulnerabilities": [
                {
                    "damage_type_id": 3,
                    "add_damage_type": False,
                }
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This damage type does not exist."}


def test_pc_fake_immunity_put(create_pc, db_session):
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={
            "immunities": [
                {
                    "damage_type_id": 3,
                    "add_damage_type": False,
                }
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This damage type does not exist."}


def test_pc_fake_advantage_put(create_pc, db_session):
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={
            "advantages": [
                {
                    "attribute_id": 3,
                    "add_attribute": False,
                }
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This attribute does not exist."}


def test_pc_fake_disadvantage_put(create_pc, db_session):
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        json={
            "disadvantages": [
                {
                    "attribute_id": 3,
                    "add_attribute": False,
                }
            ],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This attribute does not exist."}


def test_pc_delete(create_pc, db_session):
    response = client.delete(f"/api/player_characters/{create_pc.id}")
    pc = (
        db_session.query(PlayerCharacter)
        .filter(PlayerCharacter.id == create_pc.id)
        .first()
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Player character has been deleted."}
    assert pc == None


def test_pc_fake_delete(create_pc, db_session):
    response = client.delete(f"/api/player_characters/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The player character you are trying to delete does not exist."
    }
