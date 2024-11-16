from sqlalchemy import select

from server.models import Attribute
from .conftest import client


def test_no_auth_attributes():
    response = client.get("/api/attributes")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_attributes(login, create_attribute):
    token = login.get(name="user_token")
    response = client.get(
        "/api/attributes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Charmed"}]


def test_get_no_attributes(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/attributes",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_attribute(login, create_attribute):
    token = login.get(name="user_token")
    response = client.get(
        "/api/attributes/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Charmed"}


def test_get_no_attribute(login, create_attribute):
    token = login.get(name="user_token")
    response = client.get(
        "/api/attributes/2",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Attribute not found."}


def test_post_attribute(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/attributes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "attribute_name": "Charmed",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "message": "New attribute 'Charmed' has been added to the database.",
        "attribute": {"id": 1, "name": "Charmed"},
    }


def test_post_duplicate_attribute(login):
    token = login.get(name="user_token")
    client.post(
        "/api/attributes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "attribute_name": "Charmed",
        },
    )
    response = client.post(
        "/api/attributes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "attribute_name": "Charmed",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Attribute already exists."}


def test_attribute_name_put(login, create_attribute, db_session):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/attributes/{create_attribute.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"attribute_name": "Slashing"},
    )

    stmt = select(Attribute)
    attribute = db_session.execute(stmt).scalar_one_or_none()

    assert response.status_code == 200
    assert attribute.name == "Slashing"
    assert response.json() == {
        "message": "Attribute 'Slashing' has been updated.",
        "attribute": {"id": 1, "name": "Slashing"},
    }


def test_attribute_duplicate_name_put(login, create_attribute, db_session):
    token = login.get(name="user_token")

    attribute = Attribute(name="Slashing")
    db_session.add(attribute)
    db_session.commit()
    response = client.put(
        f"/api/attributes/{attribute.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"attribute_name": "Charmed"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The name you are trying to use already exists.",
    }


def test_attribute_fake_attribute_put(login, create_race, create_attribute):
    token = login.get(name="user_token")
    response = client.put(
        "/api/attributes/2",
        headers={"Authorization": f"Bearer {token}"},
        json={"attribute_name": "Slashing"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The attribute you are trying to update does not exist.",
    }


def test_attribute_delete(login, create_attribute, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/attributes/{create_attribute.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    attribute = db_session.get(Attribute, create_attribute.id)

    assert response.status_code == 200
    assert response.json() == {"message": f"Attribute has been deleted."}
    assert attribute is None


def test_attribute_fake_delete(login, create_attribute):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/attributes/2",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The attribute you are trying to delete does not exist."
    }
