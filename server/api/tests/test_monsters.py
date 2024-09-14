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
        "parties": [{"id": 1, "name": "Murder Hobo Party"}],
        "classes": [{"name": "Artificer", "id": 1}],
        "subclasses": [{"id": 1, "class_id": 1, "name": "Alchemist"}],
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


def test_monster_name_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"name": "Froghemoth"},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.name == "Froghemoth"
    assert response.json() == {
        "message": "Monster 'Froghemoth' has been updated.",
        "monster": {
            "name": "Froghemoth",
            "size_id": 1,
            "id": 1,
            "description": "A large hippo like creature",
            "creature": "monsters",
            "alive": True,
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "type_id": 1,
        },
    }


def test_monster_information_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"information": "Some new information about the big hippo."},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.information == "Some new information about the big hippo."
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "size_id": 1,
            "id": 1,
            "description": "A large hippo like creature",
            "creature": "monsters",
            "alive": True,
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some new information about the big hippo.",
            "type_id": 1,
        },
    }


def test_monster_description_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"description": "Something else about the hippo."},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.description == "Something else about the hippo."
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "size_id": 1,
            "id": 1,
            "description": "Something else about the hippo.",
            "creature": "monsters",
            "alive": True,
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "type_id": 1,
        },
    }


def test_monster_alive_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"alive": False},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.alive == False
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "active": True,
            "creature": "monsters",
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "type_id": 1,
            "id": 1,
            "name": "Giff",
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": False,
        },
    }


def test_monster_active_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"active": False},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.active == False
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "active": False,
            "creature": "monsters",
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "type_id": 1,
            "id": 1,
            "name": "Giff",
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
        },
    }


def test_monster_armour_class_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"armour_class": 20},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.armour_class == 20
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "active": True,
            "creature": "monsters",
            "armour_class": 20,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "type_id": 1,
            "id": 1,
            "name": "Giff",
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
        },
    }


def test_monster_race_put(create_monster, create_race, db_session):
    race_id = create_race.id
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"race": race_id},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.race == race_id
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": race_id,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_fake_race_put(create_monster, db_session):
    response = client.put(f"/api/monsters/{create_monster.id}", json={"race": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Race with this id does not exist."}


def test_monster_subrace_put(create_monster, create_subrace, db_session):
    subrace_id = create_subrace.id
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"subrace": subrace_id},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.subrace == subrace_id
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": subrace_id,
            "type_id": 1,
        },
    }


def test_monster_fake_subrace_put(create_monster, db_session):
    response = client.put(f"/api/monsters/{create_monster.id}", json={"subrace": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace with this id does not exist."}


def test_monster_size_put(create_monster, create_size, db_session):
    size = Size(name="Medium")
    db_session.add(size)
    db_session.commit()
    size_id = size.id
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"size_id": size_id},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.size_id == size_id
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": size_id,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_fake_size_put(create_monster, db_session):
    response = client.put(f"/api/monsters/{create_monster.id}", json={"size_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Size with this id does not exist."}


def test_monster_type_put(create_monster, create_type, db_session):
    new_type = Type(name="Celestial")
    db_session.add(new_type)
    db_session.commit()
    type_id = new_type.id
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"type_id": type_id},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert monster.type_id == type_id
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": type_id,
        },
    }


def test_monster_fake_type_put(create_monster, db_session):
    response = client.put(f"/api/monsters/{create_monster.id}", json={"type_id": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Type with this id does not exist."}


def test_monster_add_class_put(create_monster, create_class, db_session):
    new_class = Class(name="Barbarian")
    db_session.add(new_class)
    db_session.commit()
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"classes": [2], "add_class": True},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.classes) == 2
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_remove_class_put(create_monster, create_class, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"classes": [1], "add_class": False},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.classes) == 0
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_fake_class_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"classes": [3], "add_classes": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Class with this id does not exist."}


def test_monster_add_subclass_put(create_monster, create_subclass, db_session):
    new_subclass = Subclass(name="Armourer")
    db_session.add(new_subclass)
    db_session.commit()
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"subclasses": [2], "add_subclass": True},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.subclasses) == 2
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_remove_subclass_put(create_monster, create_subclass, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"subclasses": [1], "add_subclass": False},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.subclasses) == 0
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_fake_subclass_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"subclasses": [3], "add_subclasses": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass with this id does not exist."}


def test_monster_add_party_put(create_monster, create_party, db_session):
    new_party = Party(name="Hobo Helping Party")
    db_session.add(new_party)
    db_session.commit()
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"parties": [2], "add_parties": True},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.parties) == 2
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_remove_party_put(create_monster, create_party, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"parties": [1], "add_parties": False},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.parties) == 0
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_fake_part_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"parties": [3], "add_parties": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Party with this id does not exist."}


def test_monster_add_resistance_put(create_monster, db_session):
    new_resistance = Effect(name="Slashing")
    db_session.add(new_resistance)
    db_session.commit()
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"resistances": [2], "add_resistances": True},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.resistances) == 2
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_remove_resistance_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"resistances": [1], "add_resistances": False},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.resistances) == 0
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_fake_resistance_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"resistances": [3], "add_resistances": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_monster_add_vulnerability_put(create_monster, db_session):
    new_vulnerability = Effect(name="Slashing")
    db_session.add(new_vulnerability)
    db_session.commit()
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"vulnerabilities": [2], "add_vulnerabilities": True},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.vulnerabilities) == 2
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_remove_vulnerability_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"vulnerabilities": [1], "add_vulnerabilities": False},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.vulnerabilities) == 0
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_fake_vulnerability_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"vulnerabilities": [3], "add_vulnerabilities": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_monster_add_immunity_put(create_monster, db_session):
    new_immunity = Effect(name="Slashing")
    db_session.add(new_immunity)
    db_session.commit()
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"immunities": [2], "add_immunities": True},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.immunities) == 2
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_remove_immunity_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"immunities": [1], "add_immunities": False},
    )
    monster = db_session.query(Monster).first()
    assert response.status_code == 200
    assert len(monster.immunities) == 0
    assert response.json() == {
        "message": "Monster 'Giff' has been updated.",
        "monster": {
            "name": "Giff",
            "id": 1,
            "size_id": 1,
            "description": "A large hippo like creature",
            "alive": True,
            "creature": "monsters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_monster_fake_immunity_put(create_monster, db_session):
    response = client.put(
        f"/api/monsters/{create_monster.id}",
        json={"immunities": [3], "add_immunities": False},
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
