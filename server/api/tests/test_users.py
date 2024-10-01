import uuid
from fastapi.testclient import TestClient
from sqlalchemy import select

from server.database.models.player_characters import PlayerCharacter
from server.database.models.users import User
from server.database.models.roles import Role
from server.database.models.parties import Party

from .conftest import app

client = TestClient(app)


def test_get_users(create_user, db_session):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "1",
            "name": "test",
            "username": "Test",
            "image": None,
            "parties": [{"id": 1, "name": "Murder Hobo Party"}],
            "roles": [{"id": 1, "name": "Player"}],
            "characters": [],
        }
    ]


def test_get_no_users(db_session):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json() == []


def test_get_user(create_user, db_session):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "name": "test",
        "username": "Test",
        "image": None,
        "parties": [{"id": 1, "name": "Murder Hobo Party"}],
        "roles": [{"id": 1, "name": "Player"}],
        "characters": [],
    }


def test_get_no_user(create_user, db_session):
    response = client.get("/api/users/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


def test_post_user(create_party, create_role, create_pc, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "password": "Test",
            "username": "player",
            "parties": [1],
            "roles": [1],
        },
    )
    response_json = response.json()
    user_id = response_json["user"]["id"]

    assert response.status_code == 200
    assert user_id == str(uuid.UUID(user_id, version=4))
    assert response_json == {
        "message": "New user 'Player' has been added to the database.",
        "user": {
            "id": user_id,
            "name": "Player",
            "username": "player",
            "image": None,
            "parties": [{"id": 1, "name": "Murder Hobo Party"}],
            "roles": [{"id": 1, "name": "Player"}],
            "characters": [],
        },
    }


def test_post_duplicate_user(create_party, create_role, create_pc, db_session):
    client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [1],
        },
    )
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists."}


def test_post_user_fake_party(create_party, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "One or more parties not found."}


def test_post_user_fake_role(create_role, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "roles": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "One or more roles not found."}


def test_user_duplicate_username_put(
    create_user, create_role, create_party, db_session
):
    user = User(
        name="Duplicate",
        username="duplicate",
        roles=[create_role],
        parties=[create_party],
    )
    db_session.add(user)
    db_session.commit()
    response = client.put(
        f"/api/users/{user.id}",
        json={"username": "Test"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The username you are trying to use already exists.",
    }


def test_user_put(create_user, db_session):
    role = Role(name="Test Role")
    db_session.add(role)

    party = Party(name="Test Party")
    db_session.add(party)

    character = PlayerCharacter(name="Test Character", user_id=create_user.id)
    db_session.add(character)

    db_session.commit()
    db_session.refresh(role)
    db_session.refresh(character)
    db_session.refresh(party)

    response = client.put(
        f"/api/users/{create_user.id}",
        json={
            "name": "Dungeon Master",
            "username": "DM",
            "roles": [{"role_id": role.id, "add_role": True}],
            "parties": [{"party_id": party.id, "add_party": True}],
            "characters": [{"character_id": character.id, "add_character": True}],
        },
    )
    stmt = select(User)
    user = db_session.execute(stmt).scalar_one_or_none()
    assert response.status_code == 200
    assert user.name == "Dungeon Master"
    assert user.username == "DM"
    assert len(user.roles) == 2
    assert len(user.parties) == 2
    assert len(user.characters) == 1
    assert response.json() == {
        "message": "User 'Dungeon Master' has been updated.",
        "user": {
            "id": "1",
            "name": "Dungeon Master",
            "username": "DM",
            "image": None,
            "parties": [
                {"id": 1, "name": "Murder Hobo Party"},
                {"id": 2, "name": "Test Party"},
            ],
            "roles": [{"id": 1, "name": "Player"}, {"id": 2, "name": "Test Role"}],
            "characters": [
                {
                    "id": 1,
                    "name": "Test Character",
                }
            ],
        },
    }


def test_user_fake_role_put(create_user, db_session):
    response = client.put(
        f"/api/users/{create_user.id}",
        json={
            "roles": [{"role_id": 2, "add_role": True}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Role with id '2' not found.",
    }


def test_user_fake_party_put(create_user, db_session):
    response = client.put(
        f"/api/users/{create_user.id}",
        json={"parties": [{"party_id": 2, "add_party": True}]},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Party with id '2' not found.",
    }


def test_user_fake_character_put(create_user, db_session):
    response = client.put(
        f"/api/users/{create_user.id}",
        json={
            "characters": [{"character_id": 2, "add_character": True}],
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Character with id '2' not found.",
    }


def test_user_fake_user_put(create_race, create_user, db_session):
    response = client.put(
        "/api/users/2",
        json={"username": "DM"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The user you are trying to update does not exist.",
    }


def test_user_delete(create_user, db_session):
    response = client.delete(f"/api/users/{create_user.id}")
    user = db_session.get(User, create_user.id)
    assert response.status_code == 200
    assert response.json() == {"message": f"User has been deleted."}
    assert user == None


def test_user_fake_delete(create_user, db_session):
    response = client.delete(f"/api/users/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The user you are trying to delete does not exist."
    }
