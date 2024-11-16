from server.models import Attribute
from server.models import Class
from server.models import DamageType
from server.models import Party
from server.models import PlayerCharacter
from server.models import Size
from server.models import Subclass
from server.models import Type
from .conftest import client


def test_no_auth_pcs():
    response = client.get("/api/player_characters")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_pcs(login, create_pc):
    token = login.get(name="user_token")
    response = client.get(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == [
        {
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
            "user": {"id": "2", "name": "Test", "username": "test", "image": None},
        }
    ]


def test_get_no_pcs(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_pc(login, create_pc):
    token = login.get(name="user_token")
    response = client.get(
        "/api/player_characters/1",
        headers={"Authorization": f"Bearer {token}"}
    )

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
        "user": {"id": "2", "name": "Test", "username": "test", "image": None},
    }


def test_get_no_pc(login, create_pc):
    token = login.get(name="user_token")
    response = client.get("/api/player_characters/2",
                          headers={"Authorization": f"Bearer {token}"}
                          )

    assert response.status_code == 404
    assert response.json() == {"detail": "Player character not found."}


def test_post_pc(
        login,
        create_class,
        create_subclass,
        create_race,
        create_subrace,
        create_size,
        create_type,
        create_party,
        create_damage_type,
        create_attribute,
):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
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
        "message": "New pc 'Gobby' has been added to the database.",
        "pc": {
            "id": 1,
            "name": "Gobby",
            "description": "A gemstone obsessed goblin.",
            "information": "This guy reeeealy loves finding and sharing gemstones.",
            "alive": True,
            "active": True,
            "armour_class": 22,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "climbing_speed": 5,
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
            "user": {"id": "1", "name": "Admin", "username": "admin", "image": None},
        },
    }


def test_post_pc_fake_class(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "classes": [1],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found."}


def test_post_pc_fake_subclass(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "subclasses": [1],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass not found."}


def test_post_pc_fake_race(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "race_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_post_pc_fake_subrace(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "subrace_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_post_pc_fake_size(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "size_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Size not found."}


def test_post_pc_fake_type(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "type_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Type not found."}


def test_post_pc_fake_party(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "parties": [1],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Party not found."}


def test_post_pc_fake_resistance(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "resistances": [{"damage_type_id": 1, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_pc_fake_immunity(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "immunities": [{"damage_type_id": 1, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_pc_fake_vulnerabilities(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "vulnerabilities": [{"damage_type_id": 2, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_pc_fake_advantages(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "advantages": [{"attribute_id": 2, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute not found."}


def test_post_pc_fake_disadvantages(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "disadvantages": [{"attribute_id": 2, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute not found."}


def test_pc_add_put(
        login,
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

    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
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
    assert pc.race_id == race_id
    assert pc.subrace_id == subrace_id
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
        "pc": {
            "id": 1,
            "name": "Electra",
            "description": "Something else about the Electra.",
            "information": "Some new information about Electra.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "climbing_speed": 5,
            "image": None,
            "race": {"id": 1, "name": "Dwarf"},
            "subrace": {"id": 1, "name": "Duergar"},
            "size": {"id": 2, "name": "Medium"},
            "creature_type": {"id": 2, "name": "Celestial"},
            "classes": [{"id": 1, "name": "Artificer"}, {"id": 2, "name": "Barbarian"}],
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
            "user": {"id": "2", "name": "Test", "username": "test", "image": None},
        },
    }


def test_pc_remove_put(
        login,
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

    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
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
            "classes": [{"class_id": 1, "add_class": False}],
            "subclasses": [{"subclass_id": 1, "add_subclass": False}],
            "parties": [{"party_id": 1, "add_party": False}],
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
    assert pc.race_id == race_id
    assert pc.subrace_id == subrace_id
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
        "pc": {
            "id": 1,
            "name": "Electra",
            "description": "Something else about the Electra.",
            "information": "Some new information about Electra.",
            "alive": False,
            "active": False,
            "armour_class": 20,
            "walking_speed": 35,
            "swimming_speed": 30,
            "flying_speed": 5,
            "climbing_speed": 5,
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
            "user": {"id": "2", "name": "Test", "username": "test", "image": None},
        },
    }


def test_pc_fake_race_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"race_id": 3}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_pc_fake_subrace_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"subrace_id": 3}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_pc_fake_size_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"size_id": 3}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Size not found."}


def test_pc_fake_type_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"type_id": 3}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Type not found."}


def test_pc_fake_class_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "classes": [{"class_id": 3, "add_class": True}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found."}


def test_pc_fake_subclass_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subclasses": [{"subclass_id": 3, "add_subclass": True}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass not found."}


def test_pc_fake_party_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "parties": [{"party_id": 3, "add_party": True}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Party not found."}


def test_pc_fake_resistance_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
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


def test_pc_fake_vulnerability_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
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


def test_pc_fake_immunity_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
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


def test_pc_fake_advantage_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
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


def test_pc_fake_disadvantage_put(login, create_pc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
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


def test_pc_delete(login, create_pc, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/player_characters/{create_pc.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    pc = db_session.get(PlayerCharacter, create_pc.id)

    assert response.status_code == 200
    assert response.json() == {"message": "Player character has been deleted."}
    assert pc is None


def test_pc_fake_delete(login):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/player_characters/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The player character you are trying to delete does not exist."
    }
