from server.models import Attribute
from server.models import Class
from server.models import DamageType
from server.models import NonPlayerCharacter
from server.models import Party
from server.models import Size
from server.models import Subclass
from server.models import Type
from .conftest import client


def test_no_auth_npc_characters():
    response = client.get("/api/non_player_characters")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_npc_characters(login, create_npc):
    token = login.get(name="user_token")
    response = client.get(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Fersi (Oracle)",
            "description": "A demigod female.",
            "information": "Some say she knows everything, but shares very little.",
            "alive": True,
            "active": True,
            "armour_class": 16,
            "walking_speed": 30,
            "swimming_speed": 25,
            "flying_speed": 5,
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


def test_get_no_npc_characters(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_npc_character(login, create_npc):
    token = login.get(name="user_token")
    response = client.get(
        "/api/non_player_characters/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Fersi (Oracle)",
        "description": "A demigod female.",
        "information": "Some say she knows everything, but shares very little.",
        "alive": True,
        "active": True,
        "armour_class": 16,
        "walking_speed": 30,
        "swimming_speed": 25,
        "flying_speed": 5,
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


def test_get_no_npc_character(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/non_player_characters/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Non player character not found."}


def test_post_npc(
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
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "description": "Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
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
        "message": "New npc 'Volothamp Geddarm' has been added to the database.",
        "npc": {
            "id": 1,
            "name": "Volothamp Geddarm",
            "description": "Volo for short",
            "information": "A widely traveled human wizard and sage of Faerûn.",
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
        },
    }


def test_post_npc_fake_class(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "classes": [1],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found."}


def test_post_npc_fake_subclass(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "subclasses": [1],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass not found."}


def test_post_npc_fake_race(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "race_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_post_npc_fake_subrace(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "subrace_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_post_npc_fake_size(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "size_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Size not found."}


def test_post_npc_fake_type(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "type_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Type not found."}


def test_post_npc_fake_party(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "parties": [1],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Party not found."}


def test_post_npc_fake_resistance(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "resistances": [{"damage_type_id": 1, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_npc_fake_immunity(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "immunities": [{"damage_type_id": 1, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_npc_fake_vulnerabilities(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Volothamp Geddarm",
            "vulnerabilities": [{"damage_type_id": 1, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type not found."}


def test_post_npc_fake_advantages(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "advantages": [{"attribute_id": 1, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute not found."}


def test_post_npc_fake_disadvantages(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/non_player_characters",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Gobby",
            "user_id": 1,
            "disadvantages": [{"attribute_id": 1, "condition": "When in rage"}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute not found."}


def test_npc_add_put(
        login,
        create_npc,
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

    new_resistance = DamageType(name="Slashing")
    db_session.add(new_resistance)

    new_attribute = Attribute(name="Poisoned")
    db_session.add(new_attribute)

    db_session.commit()

    size_id = size.id
    type_id = new_type.id

    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Endofyre",
            "information": "Some new information about the big hippo.",
            "description": "Something else about the hippo.",
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

    npc = db_session.query(NonPlayerCharacter).first()

    assert response.status_code == 200
    assert npc.name == "Endofyre"
    assert npc.information == "Some new information about the big hippo."
    assert npc.description == "Something else about the hippo."
    assert npc.alive == False
    assert npc.active == False
    assert npc.armour_class == 20
    assert npc.walking_speed == 35
    assert npc.swimming_speed == 30
    assert npc.flying_speed == 5
    assert npc.race_id == race_id
    assert npc.subrace_id == subrace_id
    assert npc.size_id == size_id
    assert npc.type_id == type_id
    assert len(npc.classes) == 2
    assert len(npc.subclasses) == 2
    assert len(npc.parties) == 2
    assert len(npc.immunities) == 2
    assert len(npc.resistances) == 2
    assert len(npc.vulnerabilities) == 2
    assert len(npc.advantages) == 2
    assert len(npc.disadvantages) == 2
    assert response.json() == {
        "message": "NPC 'Endofyre' has been updated.",
        "npc": {
            "id": 1,
            "name": "Endofyre",
            "description": "Something else about the hippo.",
            "information": "Some new information about the big hippo.",
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
        },
    }


def test_npc_remove_put(
        login,
        create_npc,
        create_race,
        create_subrace,
        create_class,
        create_subclass,
        db_session
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
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Endofyre",
            "information": "",
            "description": "",
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

    npc = db_session.query(NonPlayerCharacter).first()

    assert response.status_code == 200
    assert npc.name == "Endofyre"
    assert npc.information == "Some say she knows everything, but shares very little."
    assert npc.description == "A demigod female."
    assert npc.alive == False
    assert npc.active == False
    assert npc.armour_class == 20
    assert npc.walking_speed == 35
    assert npc.swimming_speed == 30
    assert npc.flying_speed == 5
    assert npc.race_id == race_id
    assert npc.subrace_id == subrace_id
    assert npc.size_id == size_id
    assert npc.type_id == type_id
    assert len(npc.classes) == 0
    assert len(npc.subclasses) == 0
    assert len(npc.parties) == 0
    assert len(npc.immunities) == 0
    assert len(npc.resistances) == 0
    assert len(npc.vulnerabilities) == 0
    assert len(npc.advantages) == 0
    assert len(npc.disadvantages) == 0
    assert response.json() == {
        "message": "NPC 'Endofyre' has been updated.",
        "npc": {
            "id": 1,
            "name": "Endofyre",
            "description": "A demigod female.",
            "information": "Some say she knows everything, but shares very little.",
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
        },
    }


def test_npc_fake_race_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"race_id": 3}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_npc_fake_subrace_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"subrace_id": 3}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_npc_fake_size_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"size_id": 3}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Size not found."}


def test_npc_fake_type_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"type_id": 3}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Type not found."}


def test_npc_fake_class_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"classes": [{"class_id": 3, "add_class": False}]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found."}


def test_npc_fake_subclass_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"subclasses": [{"subclass_id": 3, "add_subclass": False}]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass not found."}


def test_npc_fake_party_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"parties": [{"party_id": 3, "add_party": False}]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Party not found."}


def test_npc_fake_resistance_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
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


def test_npc_fake_vulnerability_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
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


def test_npc_fake_immunity_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
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


def test_npc_fake_advantage_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
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


def test_npc_fake_disadvantage_put(login, create_npc):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
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


def test_npc_delete(login, create_npc, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/non_player_characters/{create_npc.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    npc = db_session.get(NonPlayerCharacter, create_npc.id)

    assert response.status_code == 200
    assert response.json() == {"message": "NPC has been deleted."}
    assert npc is None


def test_npc_fake_delete(login, create_npc):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/non_player_characters/2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The NPC you are trying to delete does not exist."
    }
