from sqlalchemy import select

from server.models import Size
from .conftest import client


def test_no_auth_sizes():
    response = client.get("/api/sizes")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_sizes(login, create_size):
    token = login.get(name="user_token")
    response = client.get(
        "/api/sizes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == [
        {"name": "Tiny", "id": 1},
    ]


def test_get_no_sizes(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/sizes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_size(login, create_size):
    token = login.get(name="user_token")
    response = client.get(
        "/api/sizes/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    print(response.json())

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Tiny"}


def test_get_no_size(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/sizes/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Size not found."}


def test_post_size(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/sizes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "size_name": "Medium",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "New size 'Medium' has been added to the database.",
        "size": {"id": 1, "name": "Medium"},
    }


def test_post_duplicate_size(login):
    token = login.get(name="user_token")
    client.post(
        "/api/sizes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "size_name": "Medium",
        },
    )
    response = client.post(
        "/api/sizes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "size_name": "Medium",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Size already exists."}


def test_size_name_put(login, create_size, db_session):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/sizes/{create_size.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"size_name": "Medium"},
    )

    stmt = select(Size)
    size = db_session.execute(stmt).scalar_one_or_none()

    assert response.status_code == 200
    assert size.name == "Medium"
    assert response.json() == {
        "message": "Size 'Medium' has been updated.",
        "size": {"id": 1, "name": "Medium"},
    }


def test_size_duplicate_name_put(login, create_size, db_session):
    size = Size(name="Small")
    db_session.add(size)
    db_session.commit()

    token = login.get(name="user_token")
    response = client.put(
        f"/api/sizes/{size.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"size_name": "Tiny"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_size_fake_size_put(login):
    token = login.get(name="user_token")
    response = client.put(
        "/api/sizes/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"size_name": "Medium"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The size you are trying to update does not exist.",
    }


def test_size_delete(login, create_size, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/sizes/{create_size.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    size = db_session.get(Size, create_size.id)

    assert response.status_code == 200
    assert response.json() == {"message": f"Size has been deleted."}
    assert size is None


def test_size_fake_delete(login):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/sizes/2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The size you are trying to delete does not exist."
    }
