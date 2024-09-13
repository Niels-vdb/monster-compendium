from fastapi.testclient import TestClient

from server.database.models.player_characters import PlayerCharacter
from server.database.models.users import Party, Role, User

from .conftest import app

client = TestClient(app)


def test_get_users(create_user, db_session):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "password": None,
                "username": "Test",
                "name": "test",
                "image": None,
            }
        ]
    }


def test_get_no_users(db_session):
    response = client.get("/api/users")
    assert response.status_code == 404
    assert response.json() == {"detail": "No users found."}


def test_get_user(create_user, db_session):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "test",
        "username": "Test",
        "image": None,
        "parties": [{"name": "Murder Hobo Party", "id": 1}],
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
            "username": "player",
            "parties": [1],
            "roles": [1],
            "characters": [1],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New user 'Player' has been added to the database.",
        "user": {
            "id": 2,
            "password": None,
            "username": "player",
            "name": "Player",
            "image": None,
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
            "characters": [1],
        },
    )
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [1],
            "characters": [1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists."}


def test_post_user_fake_party(create_party, create_role, create_pc, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [2],
            "roles": [1],
            "characters": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party, role or character you are trying to bind to this race does not exist."
    }


def test_post_user_fake_role(create_party, create_role, create_pc, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [2],
            "characters": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party, role or character you are trying to bind to this race does not exist."
    }


def test_post_user_fake_character(create_party, create_role, create_pc, db_session):
    response = client.post(
        "/api/users",
        json={
            "name": "Player",
            "username": "player",
            "parties": [1],
            "roles": [1],
            "characters": [2],
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party, role or character you are trying to bind to this race does not exist."
    }


def test_user_username_put(create_user, db_session):
    response = client.put(
        f"/api/users/{create_user.id}",
        json={"username": "DM"},
    )
    user = db_session.query(User).first()
    assert response.status_code == 200
    assert user.username == "DM"
    assert response.json() == {
        "message": "User 'test' has been updated.",
        "user": {
            "id": 1,
            "password": None,
            "username": "DM",
            "image": None,
            "name": "test",
        },
    }


def test_user_name_put(create_user, db_session):
    response = client.put(
        f"/api/users/{create_user.id}",
        json={"name": "Dungeon Master"},
    )
    user = db_session.query(User).first()
    assert response.status_code == 200
    assert user.name == "Dungeon Master"
    assert response.json() == {
        "message": "User 'Dungeon Master' has been updated.",
        "user": {
            "id": 1,
            "password": None,
            "username": "Test",
            "image": None,
            "name": "Dungeon Master",
        },
    }


def test_user_role_put(create_user, db_session):
    role = Role(name="Test Role")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)

    response = client.put(
        f"/api/users/{create_user.id}",
        json={"roles": [role.id]},
    )
    user = db_session.query(User).first()
    assert response.status_code == 200
    assert user.roles[0].id == 2
    assert response.json() == {
        "message": "User 'test' has been updated.",
        "user": {
            "id": 1,
            "password": None,
            "name": "test",
            "image": None,
            "username": "Test",
        },
    }


def test_user_fake_role_put(create_user, db_session):
    response = client.put(
        f"/api/users/{create_user.id}",
        json={"roles": [2]},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The role you are trying to link to this user does not exist.",
    }


def test_user_party_put(create_user, db_session):
    party = Party(name="Test Party")
    db_session.add(party)
    db_session.commit()
    db_session.refresh(party)

    response = client.put(
        f"/api/users/{create_user.id}",
        json={"parties": [party.id]},
    )
    user = db_session.query(User).first()
    assert response.status_code == 200
    assert user.parties[0].id == 2
    assert response.json() == {
        "message": "User 'test' has been updated.",
        "user": {
            "id": 1,
            "password": None,
            "name": "test",
            "image": None,
            "username": "Test",
        },
    }


def test_user_fake_party_put(create_user, db_session):
    response = client.put(
        f"/api/users/{create_user.id}",
        json={"parties": [2]},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party you are trying to link to this user does not exist.",
    }


def test_user_character_put(create_user, db_session):
    character = PlayerCharacter(name="Test Character", user_id=create_user.id)
    db_session.add(character)
    db_session.commit()
    db_session.refresh(character)

    response = client.put(
        f"/api/users/{create_user.id}",
        json={"characters": [character.id]},
    )
    user = db_session.query(User).first()
    assert response.status_code == 200
    assert user.characters[0].id == 1
    assert response.json() == {
        "message": "User 'test' has been updated.",
        "user": {
            "id": 1,
            "password": None,
            "name": "test",
            "image": None,
            "username": "Test",
        },
    }


def test_user_fake_character_put(create_user, db_session):
    response = client.put(
        f"/api/users/{create_user.id}",
        json={"characters": [1]},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The character you are trying to link to this user does not exist.",
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
    user = db_session.query(User).filter(User.id == create_user.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": f"User has been deleted."}
    assert user == None


def test_user_fake_delete(create_user, db_session):
    response = client.delete(f"/api/users/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The user you are trying to delete does not exist."
    }
