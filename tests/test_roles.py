from sqlalchemy import select

from server.models import Role
from .conftest import client


def test_no_auth_roles():
    response = client.get("/api/roles")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_roles(login, create_role):
    token = login.get(name="user_token")
    response = client.get(
        "/api/roles",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Player", "users": []}]


def test_get_no_roles(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/roles",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_role(login, create_role):
    token = login.get(name="user_token")
    response = client.get(
        "/api/roles/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Player", "users": []}


def test_get_no_role(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/roles/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found."}


def test_post_role(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/roles",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "role_name": "Admin",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "New role 'Admin' has been added to the database.",
        "role": {"id": 1, "name": "Admin", "users": []},
    }


def test_post_duplicate_role(login):
    token = login.get(name="user_token")
    client.post(
        "/api/roles",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "role_name": "Admin",
        },
    )
    response = client.post(
        "/api/roles",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "role_name": "Admin",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Role already exists."}


def test_role_name_put(login, create_role, db_session):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/roles/{create_role.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"role_name": "Admin"},
    )

    stmt = select(Role)
    role = db_session.execute(stmt).scalar_one_or_none()

    assert response.status_code == 200
    assert role.name == "Admin"
    assert response.json() == {
        "message": "Role 'Admin' has been updated.",
        "role": {"id": 1, "name": "Admin", "users": []},
    }


def test_role_duplicate_name_put(login, create_role, db_session):
    role = Role(name="Admin")
    db_session.add(role)
    db_session.commit()

    token = login.get(name="user_token")
    response = client.put(
        f"/api/roles/{role.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"role_name": "Player"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_role_fake_role_put(login):
    token = login.get(name="user_token")
    response = client.put(
        "/api/roles/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"role_name": "Admin"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The role you are trying to update does not exist.",
    }


def test_role_delete(login, create_role, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/roles/{create_role.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    role = db_session.get(Role, create_role.id)

    assert response.status_code == 200
    assert response.json() == {"message": f"Role has been deleted."}
    assert role is None


def test_role_fake_delete(login):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/roles/2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The role you are trying to delete does not exist."
    }
