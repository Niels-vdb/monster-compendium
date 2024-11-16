from sqlalchemy import select

from server.models import Race
from server.models import Subrace
from .conftest import client


def test_no_auth_subrace():
    response = client.get("/api/subraces")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_subraces(login, create_subrace):
    token = login.get(name="user_token")
    response = client.get(
        "/api/subraces",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Duergar",
            "resistances": [],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [],
            "disadvantages": [],
            "race": {
                "id": 1,
                "name": "Dwarf",
                "sizes": [{"id": 1, "name": "Tiny"}],
                "resistances": [],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [],
                "disadvantages": [],
            },
        }
    ]


def test_get_no_subraces(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/subraces",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_subrace(login, create_subrace):
    token = login.get(name="user_token")
    response = client.get(
        "/api/subraces/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Duergar",
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
        "advantages": [],
        "disadvantages": [],
        "race": {
            "id": 1,
            "name": "Dwarf",
            "sizes": [{"id": 1, "name": "Tiny"}],
            "resistances": [],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [],
            "disadvantages": [],
        },
    }


def test_get_no_subrace(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/subraces/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}


def test_post_subrace(
        login,
        create_subrace,
        create_damage_type,
        create_attribute,
        db_session
):
    token = login.get(name="user_token")
    response = client.post(
        "/api/subraces",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subrace_name": "Hill",
            "race_id": 1,
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
        "message": "New subrace 'Hill' has been added to the database.",
        "subrace": {
            "id": 2,
            "name": "Hill",
            "race": {
                "id": 1,
                "name": "Dwarf",
                "sizes": [{"id": 1, "name": "Tiny"}],
                "resistances": [],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [],
                "disadvantages": [],
            },
            "resistances": [{"id": 1, "name": "Fire"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
        },
    }


def test_post_duplicate_subrace(login, create_race):
    token = login.get(name="user_token")
    client.post(
        "/api/subraces",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subrace_name": "Hill",
            "race_id": 1,
        },
    )
    response = client.post(
        "/api/subraces",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subrace_name": "Hill",
            "race_id": 1,
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Subrace already exists."}


def test_post_subrace_wrong_race(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/subraces",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subrace_name": "Hill",
            "race_id": 1,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to bind to this subrace does not exist."
    }


def test_post_subrace_wrong_damage_type(login, create_subrace):
    token = login.get(name="user_token")
    response = client.post(
        "/api/subraces",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subrace_name": "Hill",
            "race_id": 1,
            "resistances": [
                {"damage_type_id": 2, "condition": "When in rage"},
            ],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with id '2' does not exist."}


def test_post_subrace_wrong_attribute(login, create_subrace):
    token = login.get(name="user_token")
    response = client.post(
        "/api/subraces",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subrace_name": "Hill",
            "race_id": 1,
            "advantages": [
                {"attribute_id": 2, "condition": "When in rage"},
            ],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute with id '2' does not exist."}


def test_subrace_put(
        login,
        create_subrace,
        create_size,
        create_damage_type,
        create_attribute,
        db_session,
):
    new_race = Race(name="Halfling", sizes=[create_size])
    db_session.add(new_race)
    db_session.commit()
    db_session.refresh(new_race)

    token = login.get(name="user_token")
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subrace_name": "Hill",
            "race_id": new_race.id,
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

    stmt = select(Subrace)
    subrace = db_session.execute(stmt).scalar_one_or_none()

    assert response.status_code == 200
    assert subrace.name == "Hill"
    assert subrace.race_id == 2
    assert len(subrace.resistances) == 1
    assert len(subrace.vulnerabilities) == 1
    assert len(subrace.immunities) == 1
    assert len(subrace.advantages) == 1
    assert len(subrace.disadvantages) == 1
    assert response.json() == {
        "message": "Subrace 'Hill' has been updated.",
        "subrace": {
            "id": 1,
            "name": "Hill",
            "race": {
                "id": 2,
                "name": "Halfling",
                "sizes": [{"id": 1, "name": "Tiny"}],
                "resistances": [],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [],
                "disadvantages": [],
            },
            "resistances": [{"id": 1, "name": "Fire"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
        },
    }


def test_subrace_duplicate_name_put(login, create_subrace, create_race, db_session):
    token = login.get(name="user_token")
    subrace = Subrace(name="Hill", race_id=1)
    db_session.add(subrace)
    db_session.commit()

    response = client.put(
        f"/api/subraces/{subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"subrace_name": "Duergar"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_subrace_fake_race_put(login, create_subrace):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"subrace_name": "Hill", "race_id": 2},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The race you are trying to link to this subrace does not exist.",
    }


def test_subrace_fake_resistance_put(login, create_subrace):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resistances": [
                {
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_subrace_fake_vulnerability_put(login, create_subrace):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "vulnerabilities": [
                {
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_subrace_fake_immunity_put(login, create_subrace):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "immunities": [
                {
                    "damage_type_id": 2,
                    "condition": "When in rage",
                    "add_damage_type": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Damage type with this id does not exist."}


def test_subrace_fake_advantage_put(login, create_subrace):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "advantages": [
                {
                    "attribute_id": 2,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute with this id does not exist."}


def test_subrace_fake_disadvantage_put(login, create_subrace):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/subraces/{create_subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "disadvantages": [
                {
                    "attribute_id": 2,
                    "condition": "When in rage",
                    "add_attribute": True,
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute with this id does not exist."}


def test_subrace_fake_subrace_put(login):
    token = login.get(name="user_token")
    response = client.put(
        "/api/subraces/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"subrace_name": "Hill"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The subrace you are trying to update does not exist.",
    }


def test_subrace_delete(login, create_subrace, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/subraces/{create_subrace.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    subrace = db_session.get(Subrace, create_subrace.id)

    assert response.status_code == 200
    assert response.json() == {"message": f"Subrace has been deleted."}
    assert subrace is None


def test_subrace_fake_delete(login):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/subraces/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The subrace you are trying to delete does not exist."
    }
