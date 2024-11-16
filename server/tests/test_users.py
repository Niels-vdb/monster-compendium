import uuid

from sqlalchemy import select

from server.models import Party
from server.models import PlayerCharacter
from server.models import Role
from server.models import User
from .conftest import client


def test_no_auth_users(login):
    response = client.get("/api/users")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_users(login):
    token = login.get(name="user_token")
    response = client.get("/api/users", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "1",
            "name": "Admin",
            "username": "admin",
            "image": None,
            "parties": [],
            "roles": [],
            "characters": [],
        }
    ]


def test_get_user(login):
    token = login.get(name="user_token")
    response = client.get("/api/users/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "name": "Admin",
        "username": "admin",
        "image": None,
        "parties": [],
        "roles": [],
        "characters": [],
    }


def test_get_no_user(login):
    token = login.get(name="user_token")
    response = client.get("/api/users/2", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


def test_post_user(login, create_party, create_role, create_pc):
    token = login.get(name="user_token")
    response = client.post(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
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


def test_post_duplicate_user(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Admin",
            "username": "admin",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists."}


def test_post_user_fake_party(login, create_party):
    token = login.get(name="user_token")
    response = client.post(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Player",
            "username": "player",
            "parties": [2],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "One or more parties not found."}


def test_post_user_fake_role(login, create_role):
    token = login.get(name="user_token")
    response = client.post(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Player",
            "username": "player",
            "roles": [2],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "One or more roles not found."}


def test_user_put(login, db_session):
    role = Role(name="Test Role")
    db_session.add(role)

    party = Party(name="Test Party")
    db_session.add(party)

    character = PlayerCharacter(name="Test Character", user_id="1")
    db_session.add(character)

    db_session.commit()
    db_session.refresh(role)
    db_session.refresh(character)
    db_session.refresh(party)

    token = login.get(name="user_token")
    response = client.put(
        f"/api/users/1",
        headers={"Authorization": f"Bearer {token}"},
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
    assert len(user.roles) == 1
    assert len(user.parties) == 1
    assert len(user.characters) == 1
    assert response.json() == {
        "message": "User 'Dungeon Master' has been updated.",
        "user": {
            "id": "1",
            "name": "Dungeon Master",
            "username": "DM",
            "image": None,
            "parties": [{"id": 1, "name": "Test Party"}],
            "roles": [{"id": 1, "name": "Test Role"}],
            "characters": [{"id": 1, "name": "Test Character"}],
        },
    }


def test_user_duplicate_username_put(
        login,
        create_role,
        create_party,
        db_session
):
    user = User(
        name="Duplicate",
        username="duplicate",
        password="password",
    )
    db_session.add(user)
    db_session.commit()

    token = login.get(name="user_token")
    response = client.put(
        f"/api/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "admin"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The username you are trying to use already exists.",
    }


def test_user_fake_role_put(login, create_user):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/users/{create_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "roles": [{"role_id": 2, "add_role": True}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Role with id '2' not found.",
    }


def test_user_fake_party_put(login, create_user):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/users/{create_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"parties": [{"party_id": 2, "add_party": True}]},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Party with id '2' not found.",
    }


def test_user_fake_character_put(login, create_user):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/users/{create_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "characters": [{"character_id": 2, "add_character": True}],
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Character with id '2' not found.",
    }


def test_user_fake_user_put(login):
    token = login.get(name="user_token")
    response = client.put(
        "/api/users/2",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "DM"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The user you are trying to update does not exist.",
    }


def test_user_delete(login, create_user, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/users/{create_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    user = db_session.get(User, create_user.id)

    assert response.status_code == 200
    assert response.json() == {"message": f"User has been deleted."}
    assert user is None


def test_user_fake_delete(login):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/users/2",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The user you are trying to delete does not exist."
    }
