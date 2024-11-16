from sqlalchemy import select

from server.models import Race
from .conftest import client


def test_no_auth_races():
    response = client.get("/api/races")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_races(login, create_race):
    token = login.get(name="user_token")
    response = client.get(
        "/api/races",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Dwarf",
            "sizes": [{"id": 1, "name": "Tiny"}],
            "subraces": [],
            "resistances": [],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [],
            "disadvantages": [],
        }
    ]


def test_get_no_races(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/races",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_race(login, create_race):
    token = login.get(name="user_token")
    response = client.get(
        "/api/races/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Dwarf",
        "sizes": [{"id": 1, "name": "Tiny"}],
        "subraces": [],
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
        "advantages": [],
        "disadvantages": [],
    }


def test_get_no_race(login, create_race):
    token = login.get(name="user_token")
    response = client.get(
        "/api/races/2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Race not found."}


def test_post_race(
        login,
        create_size,
        create_damage_type,
        create_attribute,
        db_session
):
    token = login.get(name="user_token")
    response = client.post(
        "/api/races",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [
                {"damage_type_id": 1, "condition": "When in rage"},
            ],
            "immunities": [
                {"damage_type_id": 1, "condition": "When not in rage"},
            ],
            "vulnerabilities": [
                {"damage_type_id": 1, "condition": "When wearing armour"},
            ],
            "advantages": [
                {"attribute_id": 1, "condition": "When wearing a shield"},
            ],
            "disadvantages": [
                {"attribute_id": 1, "condition": "When not wearing a shield"},
            ],
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "New race 'Locathah' has been added to the database.",
        "race": {
            "id": 1,
            "name": "Locathah",
            "sizes": [{"id": 1, "name": "Tiny"}],
            "subraces": [],
            "resistances": [{"id": 1, "name": "Fire"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
        },
    }


def test_post_duplicate_race(login, create_size):
    token = login.get(name="user_token")
    client.post(
        "/api/races",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "race_name": "Locathah",
            "sizes": [1],
        },
    )
    response = client.post(
        "/api/races",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "race_name": "Locathah",
            "sizes": [1],
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Race already exists."}


def test_post_race_wrong_size(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/races",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "race_name": "Locathah",
            "sizes": [1],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "One or more sizes not found."}


def test_post_race_wrong_damage_type(login, create_size):
    token = login.get(name="user_token")
    response = client.post(
        "/api/races",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "resistances": [
                {"damage_type_id": 1, "condition": "When in rage"},
            ],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with id '1' does not exist."}


def test_post_race_wrong_attribute(login, create_size):
    token = login.get(name="user_token")
    response = client.post(
        "/api/races",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "race_name": "Locathah",
            "sizes": [1],
            "advantages": [
                {"attribute_id": 1, "condition": "When in rage"},
            ],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute with id '1' does not exist."}


def test_race_put(
        login,
        create_race,
        create_damage_type,
        create_attribute,
        create_size,
        db_session
):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/races/{create_race.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "race_name": "Elf",
            "sizes": [1],
            "resistances": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ],
            "vulnerabilities": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ],
            "immunities": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ],
            "advantages": [
                {
                    "attribute_id": 1,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ],
            "disadvantages": [
                {
                    "attribute_id": 1,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ],
        },
    )

    stmt = select(Race)
    race = db_session.execute(stmt).scalar_one_or_none()

    assert response.status_code == 200
    assert race.name == "Elf"
    assert race.sizes[0].id == 1
    assert len(race.resistances) == 1
    assert len(race.vulnerabilities) == 1
    assert len(race.immunities) == 1
    assert len(race.advantages) == 1
    assert len(race.disadvantages) == 1
    assert response.json() == {
        "message": "Race 'Elf' has been updated.",
        "race": {
            "id": 1,
            "name": "Elf",
            "sizes": [{"id": 1, "name": "Tiny"}],
            "subraces": [],
            "resistances": [{"id": 1, "name": "Fire"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
        },
    }


def test_race_duplicate_name_put(
        login,
        create_size,
        create_race,
        db_session
):
    race = Race(name="Elf", sizes=[create_size])
    db_session.add(race)
    db_session.commit()

    token = login.get(name="user_token")
    response = client.put(
        f"/api/races/{race.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"race_name": "Dwarf"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_race_fake_resistance_put(login, create_race):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/races/{create_race.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resistances": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_race_fake_vulnerability_put(login, create_race):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/races/{create_race.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "vulnerabilities": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_race_fake_immunity_put(login, create_race):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/races/{create_race.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "immunities": [
                {
                    "damage_type_id": 1,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_race_fake_advantage_put(login, create_race):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/races/{create_race.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "advantages": [
                {
                    "attribute_id": 1,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute with this id does not exist."}


def test_race_fake_disadvantage_put(login, create_race):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/races/{create_race.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "disadvantages": [
                {
                    "attribute_id": 1,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute with this id does not exist."}


def test_race_fake_size_put(login, create_race):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/races/{create_race.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"sizes": [2]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "One or more sizes not found."}


def test_fake_race_put(login):
    token = login.get(name="user_token")
    response = client.put(
        "/api/races/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"race_name": "Elf"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to update does not exist.",
    }


def test_race_delete(login, create_race, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/races/{create_race.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    race = db_session.get(Race, create_race.id)

    assert response.status_code == 200
    assert response.json() == {"message": "Race has been deleted."}
    assert race is None


def test_race_fake_delete(login):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/races/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to delete does not exist."
    }
