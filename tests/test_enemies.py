from typing import Any
from fastapi.testclient import TestClient
from sqlalchemy import select

from server.models import Size
from server.models import Type
from server.models import Class
from server.models import Subclass
from server.models import DamageType
from server.models import Attribute
from server.models import Enemy
from server.models import Party

from .conftest import app


client = TestClient(app)


def test_get_enemies(create_enemy, db_session):
    response = client.get("/api/enemies")
    assert response.status_code == 200
    assert response.json() == [
        {
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
            "climbing_speed": None,
            "image": None,
            "race": None,
            "subrace": None,
            "size": {"id": 1, "name": "Tiny"},
            "creature_type": {"id": 1, "name": "Aberration"},
            "classes": [{"id": 1, "name": "Artificer"}],
            "subclasses": [{"id": 1, "name": "Alchemist"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "resistances": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
        }
    ]


def test_get_no_enemies(db_session):
    response = client.get("/api/enemies")
    assert response.status_code == 200
    assert response.json() == []


def test_get_enemy(create_enemy, db_session):
    response = client.get("/api/enemies/1")
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
        "climbing_speed": None,
        "image": None,
        "race": None,
        "subrace": None,
        "size": {"id": 1, "name": "Tiny"},
        "creature_type": {"id": 1, "name": "Aberration"},
        "classes": [{"id": 1, "name": "Artificer"}],
        "subclasses": [{"id": 1, "name": "Alchemist"}],
        "immunities": [{"id": 1, "name": "Fire"}],
        "resistances": [{"id": 1, "name": "Fire"}],
        "vulnerabilities": [{"id": 1, "name": "Fire"}],
        "advantages": [{"id": 1, "name": "Charmed"}],
        "disadvantages": [{"id": 1, "name": "Charmed"}],
    }


def test_get_no_enemy(create_enemy, db_session):
    response = client.get("/api/enemies/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Enemy not found."}


def test_post_enemy(
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
        "/api/enemies",
        json={
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "walking_speed": 35,
            "swimming_speed": 35,
            "flying_speed": 35,
            "climbing_speed": 35,
            "classes": [1],
            "subclasses": [1],
            "race_id": 1,
            "subrace_id": 1,
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
    assert response.status_code == 201
    assert response.json() == {
        "message": "New enemy 'Giff' has been added to the database.",
        "enemy": {
            "id": 1,
            "name": "Giff",
            "description": " A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "walking_speed": 35,
            "swimming_speed": 35,
            "flying_speed": 35,
            "climbing_speed": 35,
            "image": None,
            "race": {"id": 1, "name": "Dwarf"},
            "subrace": {"id": 1, "name": "Duergar"},
            "size": {"id": 1, "name": "Tiny"},
            "creature_type": {"id": 1, "name": "Aberration"},
            "classes": [{"id": 1, "name": "Artificer"}],
            "subclasses": [{"id": 1, "name": "Alchemist"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "resistances": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
        },
    }


def test_post_enemy_fake_class(
    create_class,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "classes": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found."}


def test_post_enemy_fake_subclass(
    create_subclass,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "subclasses": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass not found."}


def test_post_enemy_fake_race(
    create_race,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "race_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_post_enemy_fake_subrace(
    create_subrace,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "subrace_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_post_enemy_fake_size(
    create_size,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "size_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Size not found."}


def test_post_enemy_fake_type(
    create_type,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "type_id": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Type not found."}


def test_post_enemy_fake_party(
    create_party,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "parties": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Party not found."}


def test_post_enemy_fake_resistance(
    create_damage_type,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "resistances": [{"damage_type_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_enemy_fake_immunity(
    create_damage_type,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "immunities": [{"damage_type_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_enemy_fake_vulnerabilities(
    create_damage_type,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "vulnerabilities": [{"damage_type_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_enemy_fake_advantages(
    create_user,
    create_attribute,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "user_id": 1,
            "advantages": [{"attribute_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute not found."}


def test_post_enemy_fake_disadvantages(
    create_user,
    create_attribute,
    db_session,
):
    response = client.post(
        "/api/enemies",
        json={
            "name": "Giff",
            "user_id": 1,
            "disadvantages": [{"attribute_id": 2, "condition": "When in rage"}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute not found."}


def test_enemy_add_put(
    create_enemy,
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

    new_subclass = Subclass(name="Armourer", class_id=2)
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
        f"/api/enemies/{create_enemy.id}",
        json={
            "name": "Froghemoth",
            "information": "Some new information about Froghemoth.",
            "description": "Something else about the Froghemoth.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 40,
            "swimming_speed": 40,
            "climbing_speed": 40,
            "flying_speed": 5,
            "race_id": race_id,
            "subrace_id": subrace_id,
            "size_id": size_id,
            "type_id": type_id,
            "classes": [{"class_id": 2, "add_class": True}],
            "subclasses": [{"subclass_id": 2, "add_subclass": True}],
            "parties": [{"party_id": 2, "add_party": True}],
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
    stmt = select(Enemy)
    enemy = db_session.execute(stmt).scalar_one_or_none()
    assert response.status_code == 200
    assert enemy.name == "Froghemoth"
    assert enemy.information == "Some new information about Froghemoth."
    assert enemy.description == "Something else about the Froghemoth."
    assert enemy.alive == False
    assert enemy.active == False
    assert enemy.armour_class == 20
    assert enemy.walking_speed == 40
    assert enemy.swimming_speed == 40
    assert enemy.climbing_speed == 40
    assert enemy.flying_speed == 5
    assert enemy.race_id == race_id
    assert enemy.subrace_id == subrace_id
    assert enemy.size_id == size_id
    assert enemy.type_id == type_id
    assert len(enemy.classes) == 2
    assert len(enemy.subclasses) == 2
    assert len(enemy.parties) == 2
    assert len(enemy.immunities) == 2
    assert len(enemy.resistances) == 2
    assert len(enemy.vulnerabilities) == 2
    assert len(enemy.advantages) == 2
    assert len(enemy.disadvantages) == 2
    assert response.json() == {
        "message": "Enemy 'Froghemoth' has been updated.",
        "enemy": {
            "id": 1,
            "name": "Froghemoth",
            "description": "Something else about the Froghemoth.",
            "information": "Some new information about Froghemoth.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 40,
            "swimming_speed": 40,
            "flying_speed": 5,
            "climbing_speed": 40,
            "image": None,
            "race": {"id": 1, "name": "Dwarf"},
            "subrace": {"id": 1, "name": "Duergar"},
            "size": {"id": 2, "name": "Medium"},
            "creature_type": {"id": 2, "name": "Celestial"},
            "classes": [
                {"id": 1, "name": "Artificer"},
                {"id": 2, "name": "Barbarian"},
            ],
            "subclasses": [
                {"id": 1, "name": "Alchemist"},
                {"id": 2, "name": "Armourer"},
            ],
            "immunities": [{"id": 1, "name": "Fire"}, {"id": 2, "name": "Slashing"}],
            "resistances": [{"id": 1, "name": "Fire"}, {"id": 2, "name": "Slashing"}],
            "vulnerabilities": [
                {"id": 1, "name": "Fire"},
                {"id": 2, "name": "Slashing"},
            ],
            "advantages": [{"id": 1, "name": "Charmed"}, {"id": 2, "name": "Poisoned"}],
            "disadvantages": [
                {"id": 1, "name": "Charmed"},
                {"id": 2, "name": "Poisoned"},
            ],
        },
    }


def test_enemy_remove_put(
    create_enemy,
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
        f"/api/enemies/{create_enemy.id}",
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
            "climbing_speed": 30,
            "race_id": race_id,
            "subrace_id": subrace_id,
            "size_id": size_id,
            "type_id": type_id,
            "classes": [
                {
                    "class_id": 1,
                    "add_class": False,
                }
            ],
            "subclasses": [
                {
                    "subclass_id": 1,
                    "add_subclass": False,
                }
            ],
            "parties": [
                {
                    "party_id": 1,
                    "add_party": False,
                }
            ],
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
    stmt = select(Enemy)
    enemy = db_session.execute(stmt).scalar_one_or_none()
    assert response.status_code == 200
    assert enemy.name == "Froghemoth"
    assert enemy.information == "Some new information about Froghemoth."
    assert enemy.description == "Something else about the Froghemoth."
    assert enemy.alive == False
    assert enemy.active == False
    assert enemy.armour_class == 20
    assert enemy.walking_speed == 35
    assert enemy.swimming_speed == 30
    assert enemy.flying_speed == 5
    assert enemy.climbing_speed == 30
    assert enemy.race_id == race_id
    assert enemy.subrace_id == subrace_id
    assert enemy.size_id == size_id
    assert enemy.type_id == type_id
    assert len(enemy.classes) == 0
    assert len(enemy.subclasses) == 0
    assert len(enemy.parties) == 0
    assert len(enemy.immunities) == 0
    assert len(enemy.resistances) == 0
    assert len(enemy.vulnerabilities) == 0
    assert len(enemy.advantages) == 0
    assert len(enemy.disadvantages) == 0
    assert response.json() == {
        "message": "Enemy 'Froghemoth' has been updated.",
        "enemy": {
            "id": 1,
            "name": "Froghemoth",
            "description": "Something else about the Froghemoth.",
            "information": "Some new information about Froghemoth.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "climbing_speed": 30,
            "image": None,
            "race": {"id": 1, "name": "Dwarf"},
            "subrace": {"id": 1, "name": "Duergar"},
            "size": {"id": 2, "name": "Medium"},
            "creature_type": {"id": 2, "name": "Celestial"},
            "classes": [],
            "subclasses": [],
            "immunities": [],
            "resistances": [],
            "vulnerabilities": [],
            "advantages": [],
            "disadvantages": [],
        },
    }


def test_enemy_fake_race_put(create_enemy, db_session):
    response = client.put(f"/api/enemies/{create_enemy.id}", json={"race_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_enemy_fake_subrace_put(create_enemy, db_session):
    response = client.put(f"/api/enemies/{create_enemy.id}", json={"subrace_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_enemy_fake_size_put(create_enemy, db_session):
    response = client.put(f"/api/enemies/{create_enemy.id}", json={"size_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Size not found."}


def test_enemy_fake_type_put(create_enemy, db_session):
    response = client.put(f"/api/enemies/{create_enemy.id}", json={"type_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Type not found."}


def test_enemy_fake_class_put(create_enemy, db_session):
    response = client.put(
        f"/api/enemies/{create_enemy.id}",
        json={"classes": [{"class_id": 3, "add_class": False}]},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found."}


def test_enemy_fake_subclass_put(create_enemy, db_session):
    response = client.put(
        f"/api/enemies/{create_enemy.id}",
        json={"subclasses": [{"subclass_id": 3, "add_subclass": False}]},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass not found."}


def test_enemy_fake_party_put(create_enemy, db_session):
    response = client.put(
        f"/api/enemies/{create_enemy.id}",
        json={"parties": [{"party_id": 3, "add_party": False}]},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Party not found."}


def test_enemy_fake_resistance_put(create_enemy, db_session):
    response = client.put(
        f"/api/enemies/{create_enemy.id}",
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
    assert response.json() == {"detail": "Damage type not found."}


def test_enemy_fake_vulnerability_put(create_enemy, db_session):
    response = client.put(
        f"/api/enemies/{create_enemy.id}",
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
    assert response.json() == {"detail": "Damage type not found."}


def test_enemy_fake_immunity_put(create_enemy, db_session):
    response = client.put(
        f"/api/enemies/{create_enemy.id}",
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
    assert response.json() == {"detail": "Damage type not found."}


def test_enemy_fake_advantage_put(create_enemy, db_session):
    response = client.put(
        f"/api/enemies/{create_enemy.id}",
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
    assert response.json() == {"detail": "Attribute not found."}


def test_enemy_fake_disadvantage_put(create_enemy, db_session):
    response = client.put(
        f"/api/enemies/{create_enemy.id}",
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
    assert response.json() == {"detail": "Attribute not found."}


def test_enemy_delete(create_enemy, db_session):
    response = client.delete(f"/api/enemies/{create_enemy.id}")
    enemy = db_session.get(Enemy, create_enemy.id)
    assert response.status_code == 200
    assert response.json() == {"message": "Enemy has been deleted."}
    assert enemy == None


def test_enemy_fake_delete(create_enemy, db_session):
    response = client.delete(f"/api/enemies/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The enemy you are trying to delete does not exist."
    }
