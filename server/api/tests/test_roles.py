from fastapi.testclient import TestClient

from server.database.models.users import Role

from .conftest import app


client = TestClient(app)


def test_get_roles(create_role, db_session):
    response = client.get("/api/roles")
    assert response.status_code == 200
    assert response.json() == {
        "roles": [
            {"id": 1, "name": "Player"},
        ]
    }


def test_get_no_roles(db_session):
    response = client.get("/api/roles")
    assert response.status_code == 404
    assert response.json() == {"detail": "No roles found."}


def test_get_role(create_role, db_session):
    response = client.get("/api/roles/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Player",
        "users": [],
    }


def test_get_no_role(create_role, db_session):
    response = client.get("/api/roles/1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found."}


def test_post_role(db_session):
    response = client.post(
        "/api/roles",
        json={
            "role_name": "Admin",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New role 'Admin' has been added to the database.",
        "role": {"name": "Admin", "id": 1},
    }


def test_post_duplicate_role(db_session):
    client.post(
        "/api/roles",
        json={
            "role_name": "Admin",
        },
    )
    response = client.post(
        "/api/roles",
        json={
            "role_name": "Admin",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Role already exists."}


def test_role_name_put(create_role, db_session):
    response = client.put(
        f"/api/roles/{create_role.id}",
        json={"role_name": "Admin"},
    )
    role = db_session.query(Role).first()
    assert response.status_code == 200
    assert role.name == "Admin"
    assert response.json() == {
        "message": "Role 'Admin' has been updated.",
        "role": {"id": 1, "name": "Admin"},
    }


def test_role_duplicate_name_put(create_role, db_session):
    role = Role(name="Admin")
    db_session.add(role)
    db_session.commit()
    response = client.put(
        f"/api/roles/{role.id}",
        json={"role_name": "Player"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_role_fake_role_put(create_race, create_role, db_session):
    response = client.put(
        "/api/roles/2",
        json={"role_name": "Admin"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The role you are trying to update does not exist.",
    }


def test_role_delete(create_role, db_session):
    response = client.delete(f"/api/roles/{create_role.id}")
    role = db_session.query(Role).filter(Role.id == create_role.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": f"Role has been deleted."}
    assert role == None


def test_role_fake_delete(create_role, db_session):
    response = client.delete(f"/api/roles/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The role you are trying to delete does not exist."
    }
