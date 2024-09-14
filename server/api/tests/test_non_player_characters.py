from fastapi.testclient import TestClient

from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.effects import Effect
from server.database.models.non_player_characters import NonPlayerCharacter
from server.database.models.users import Party

from .conftest import app


client = TestClient(app)


def test_get_npc_characters(create_npc, db_session):
    response = client.get("/api/non_player_characters")
    assert response.status_code == 200
    assert response.json() == {
        "non_player_characters": [
            {
                "information": "Some say she knows everything, but shares very little.",
                "subrace": None,
                "type_id": 1,
                "name": "Fersi (Oracle)",
                "size_id": 1,
                "description": "A demigod female.",
                "alive": True,
                "creature": "non_player_characters",
                "active": True,
                "id": 1,
                "armour_class": 16,
                "image": None,
                "race": None,
            }
        ]
    }


def test_get_no_npc_characters(db_session):
    response = client.get("/api/non_player_characters")
    assert response.status_code == 404
    assert response.json() == {"detail": "No NPC's found."}


def test_get_npc_character(create_npc, db_session):
    response = client.get("/api/non_player_characters/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Fersi (Oracle)",
        "description": "A demigod female.",
        "information": "Some say she knows everything, but shares very little.",
        "active": True,
        "alive": True,
        "armour_class": 16,
        "image": None,
        "race": None,
        "subrace": None,
        "size": {"id": 1, "name": "Tiny"},
        "type": 1,
        "creature_type": {"name": "Aberration", "id": 1},
        "parties": [{"id": 1, "name": "Murder Hobo Party"}],
        "classes": [{"id": 1, "name": "Artificer"}],
        "subclasses": [{"id": 1, "name": "Alchemist", "class_id": 1}],
        "resistances": [{"id": 1, "name": "Fire"}],
        "immunities": [{"id": 1, "name": "Fire"}],
        "vulnerabilities": [{"id": 1, "name": "Fire"}],
    }


def test_get_no_npc_character(create_npc, db_session):
    response = client.get("/api/non_player_characters/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "NPC not found."}


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
            "description": "Volo for short",
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
        "non_player_character": {
            "description": "Volo for short",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "id": 1,
            "armour_class": 22,
            "image": None,
            "race": 1,
            "information": "A widely traveled human wizard and sage of Faerûn.",
            "subrace": 1,
            "type_id": 1,
            "name": "Volothamp Geddarm",
            "size_id": 1,
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


def test_npc_name_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"name": "Endofyre"},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.name == "Endofyre"
    assert response.json() == {
        "message": "NPC 'Endofyre' has been updated.",
        "non_player_character": {
            "name": "Endofyre",
            "size_id": 1,
            "id": 1,
            "description": "A demigod female.",
            "creature": "non_player_characters",
            "alive": True,
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some say she knows everything, but shares very little.",
            "type_id": 1,
        },
    }


def test_npc_information_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"information": "Some new information about the big hippo."},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.information == "Some new information about the big hippo."
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "size_id": 1,
            "id": 1,
            "description": "A demigod female.",
            "creature": "non_player_characters",
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


def test_npc_description_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"description": "Something else about the hippo."},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.description == "Something else about the hippo."
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "size_id": 1,
            "id": 1,
            "description": "Something else about the hippo.",
            "creature": "non_player_characters",
            "alive": True,
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some say she knows everything, but shares very little.",
            "type_id": 1,
        },
    }


def test_npc_alive_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"alive": False},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.alive == False
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "active": True,
            "creature": "non_player_characters",
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some say she knows everything, but shares very little.",
            "type_id": 1,
            "id": 1,
            "name": "Fersi (Oracle)",
            "size_id": 1,
            "description": "A demigod female.",
            "alive": False,
        },
    }


def test_npc_active_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"active": False},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.active == False
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "active": False,
            "creature": "non_player_characters",
            "armour_class": 16,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some say she knows everything, but shares very little.",
            "type_id": 1,
            "id": 1,
            "name": "Fersi (Oracle)",
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
        },
    }


def test_npc_armour_class_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"armour_class": 20},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.armour_class == 20
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "active": True,
            "creature": "non_player_characters",
            "armour_class": 20,
            "image": None,
            "race": None,
            "subrace": None,
            "information": "Some say she knows everything, but shares very little.",
            "type_id": 1,
            "id": 1,
            "name": "Fersi (Oracle)",
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
        },
    }


def test_npc_race_put(create_npc, create_race, db_session):
    race_id = create_race.id
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"race": race_id},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.race == race_id
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": race_id,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_fake_race_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}", json={"race": 3}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Race with this id does not exist."}


def test_npc_subrace_put(create_npc, create_subrace, db_session):
    subrace_id = create_subrace.id
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"subrace": subrace_id},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.subrace == subrace_id
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": subrace_id,
            "type_id": 1,
        },
    }


def test_npc_fake_subrace_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}", json={"subrace": 3}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace with this id does not exist."}


def test_npc_size_put(create_npc, create_size, db_session):
    size = Size(name="Medium")
    db_session.add(size)
    db_session.commit()
    size_id = size.id
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"size_id": size_id},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.size_id == size_id
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": size_id,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_fake_size_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}", json={"size_id": 3}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Size with this id does not exist."}


def test_npc_type_put(create_npc, create_type, db_session):
    new_type = Type(name="Celestial")
    db_session.add(new_type)
    db_session.commit()
    type_id = new_type.id
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"type_id": type_id},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert npc.type_id == type_id
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": type_id,
        },
    }


def test_npc_fake_type_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}", json={"type_id": 3}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Type with this id does not exist."}


def test_npc_add_class_put(create_npc, create_class, db_session):
    new_class = Class(name="Barbarian")
    db_session.add(new_class)
    db_session.commit()
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"classes": [2], "add_class": True},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.classes) == 2
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_remove_class_put(create_npc, create_class, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"classes": [1], "add_class": False},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.classes) == 0
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_fake_class_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"classes": [3], "add_classes": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Class with this id does not exist."}


def test_npc_add_subclass_put(create_npc, create_subclass, db_session):
    new_subclass = Subclass(name="Armourer")
    db_session.add(new_subclass)
    db_session.commit()
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"subclasses": [2], "add_subclass": True},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.subclasses) == 2
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_remove_subclass_put(create_npc, create_subclass, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"subclasses": [1], "add_subclass": False},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.subclasses) == 0
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_fake_subclass_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"subclasses": [3], "add_subclasses": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Subclass with this id does not exist."}


def test_npc_add_party_put(create_npc, create_party, db_session):
    new_party = Party(name="Hobo Helping Party")
    db_session.add(new_party)
    db_session.commit()
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"parties": [2], "add_parties": True},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.parties) == 2
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_remove_party_put(create_npc, create_party, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"parties": [1], "add_parties": False},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.parties) == 0
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_fake_part_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"parties": [3], "add_parties": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Party with this id does not exist."}


def test_npc_add_resistance_put(create_npc, db_session):
    new_resistance = Effect(name="Slashing")
    db_session.add(new_resistance)
    db_session.commit()
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"resistances": [2], "add_resistances": True},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.resistances) == 2
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_remove_resistance_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"resistances": [1], "add_resistances": False},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.resistances) == 0
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_fake_resistance_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"resistances": [3], "add_resistances": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_npc_add_vulnerability_put(create_npc, db_session):
    new_vulnerability = Effect(name="Slashing")
    db_session.add(new_vulnerability)
    db_session.commit()
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"vulnerabilities": [2], "add_vulnerabilities": True},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.vulnerabilities) == 2
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_remove_vulnerability_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"vulnerabilities": [1], "add_vulnerabilities": False},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.vulnerabilities) == 0
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_fake_vulnerability_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"vulnerabilities": [3], "add_vulnerabilities": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_npc_add_immunity_put(create_npc, db_session):
    new_immunity = Effect(name="Slashing")
    db_session.add(new_immunity)
    db_session.commit()
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"immunities": [2], "add_immunities": True},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.immunities) == 2
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_remove_immunity_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"immunities": [1], "add_immunities": False},
    )
    npc = db_session.query(NonPlayerCharacter).first()
    assert response.status_code == 200
    assert len(npc.immunities) == 0
    assert response.json() == {
        "message": "NPC 'Fersi (Oracle)' has been updated.",
        "non_player_character": {
            "name": "Fersi (Oracle)",
            "id": 1,
            "size_id": 1,
            "description": "A demigod female.",
            "alive": True,
            "creature": "non_player_characters",
            "active": True,
            "armour_class": 16,
            "image": None,
            "race": None,
            "information": "Some say she knows everything, but shares very little.",
            "subrace": None,
            "type_id": 1,
        },
    }


def test_npc_fake_immunity_put(create_npc, db_session):
    response = client.put(
        f"/api/non_player_characters/{create_npc.id}",
        json={"immunities": [3], "add_immunities": False},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Effect with this id does not exist."}


def test_npc_delete(create_npc, db_session):
    response = client.delete(f"/api/non_player_characters/{create_npc.id}")
    npc = (
        db_session.query(NonPlayerCharacter)
        .filter(NonPlayerCharacter.id == create_npc.id)
        .first()
    )
    assert response.status_code == 200
    assert response.json() == {"message": "NPC has been deleted."}
    assert npc == None


def test_npc_fake_delete(create_npc, db_session):
    response = client.delete(f"/api/non_player_characters/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The NPC you are trying to delete does not exist."
    }
