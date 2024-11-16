from sqlalchemy import select

from server.models import Party
from .conftest import client


def test_no_auth_parties():
    response = client.get("/api/parties")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_parties(login, create_party):
    token = login.get(name="user_token")
    response = client.get(
        "/api/parties",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            'id': 1, 'name': 'Murder Hobo Party',
            'users': [],
            'creatures': []
        }
    ]


def test_get_no_parties(login):
    token = login.get(name="user_token")
    response = client.get(
        "/api/parties",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_party(login, create_party):
    token = login.get(name="user_token")
    response = client.get(
        "/api/parties/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Murder Hobo Party",
        "users": [],
        "creatures": [],
    }


def test_get_no_party(login, create_party):
    token = login.get(name="user_token")
    response = client.get(
        "/api/parties/2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Party not found."}


def test_post_party(login):
    token = login.get(name="user_token")
    response = client.post(
        "/api/parties",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "party_name": "Murder Hobo Party",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "New party 'Murder Hobo Party' has been added to the database.",
        "party": {
            "name": "Murder Hobo Party",
            "id": 1,
            "users": [],
            "creatures": [],
        },
    }


def test_party_name_put(login, create_party, db_session):
    token = login.get(name="user_token")
    response = client.put(
        f"/api/parties/{create_party.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"party_name": "Children of Truth"},
    )

    stmt = select(Party)
    party = db_session.execute(stmt).scalar_one_or_none()

    assert response.status_code == 200
    assert party.name == "Children of Truth"
    assert response.json() == {
        "message": "Party 'Children of Truth' has been updated.",
        "party": {
            "id": 1,
            "name": "Children of Truth",
            "users": [],
            "creatures": [],
        },
    }


def test_fake_party_put(login, create_party):
    token = login.get(name="user_token")
    response = client.put(
        "/api/parties/2",
        headers={"Authorization": f"Bearer {token}"},
        json={"party_name": "Children of Truth"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party you are trying to update does not exist.",
    }


def test_party_delete(login, create_party, db_session):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/parties/{create_party.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    cls = db_session.get(Party, create_party.id)

    assert response.status_code == 200
    assert response.json() == {"message": "Party has been deleted."}
    assert cls is None


def test_party_fake_delete(login, create_party):
    token = login.get(name="user_token")
    response = client.delete(
        f"/api/parties/2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party you are trying to delete does not exist."
    }
