from fastapi.testclient import TestClient
from sqlalchemy import select

from server.models import Party

from .conftest import app


client = TestClient(app)


def test_get_parties(create_party, db_session):
    response = client.get("/api/parties")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Murder Hobo Party",
            "id": 1,
            "users": [],
            "creatures": [],
        }
    ]


def test_get_no_parties(db_session):
    response = client.get("/api/parties")
    assert response.status_code == 200
    assert response.json() == []


def test_get_party(create_party, db_session):
    response = client.get("/api/parties/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Murder Hobo Party",
        "users": [],
        "creatures": [],
    }


def test_get_no_party(create_party, db_session):
    response = client.get("/api/parties/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Party not found."}


def test_post_party(db_session):
    response = client.post(
        "/api/parties",
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


def test_party_name_put(create_party, db_session):
    response = client.put(
        f"/api/parties/{create_party.id}",
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


def test_fake_party_put(create_party, db_session):
    response = client.put(
        "/api/parties/2",
        json={"party_name": "Children of Truth"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party you are trying to update does not exist.",
    }


def test_party_delete(create_party, db_session):
    response = client.delete(f"/api/parties/{create_party.id}")
    cls = db_session.get(Party, create_party.id)
    assert response.status_code == 200
    assert response.json() == {"message": "Party has been deleted."}
    assert cls == None


def test_party_delete(create_party, db_session):
    response = client.delete(f"/api/parties/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party you are trying to delete does not exist."
    }
