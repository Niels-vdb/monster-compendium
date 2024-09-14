from fastapi.testclient import TestClient

from server.database.models.users import Party

from .conftest import app


client = TestClient(app)


def test_get_parties(create_party, db_session):
    response = client.get("/api/parties")
    assert response.status_code == 200
    assert response.json() == {"parties": [{"name": "Murder Hobo Party", "id": 1}]}


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
    assert response.status_code == 200
    assert response.json() == {
        "message": "New party 'Murder Hobo Party' has been added to the database.",
        "party": {"name": "Murder Hobo Party", "id": 1},
    }


def test_party_name_put(create_party, db_session):
    response = client.put(
        f"/api/parties/{create_party.id}",
        json={"party_name": "Helping Hobo Party"},
    )
    cls = db_session.query(Party).first()
    assert response.status_code == 200
    assert cls.name == "Helping Hobo Party"
    assert response.json() == {
        "message": "Party 'Helping Hobo Party' has been updated.",
        "party": {"id": 1, "name": "Helping Hobo Party"},
    }


def test_fake_party_put(create_party, db_session):
    response = client.put(
        "/api/parties/2",
        json={"party_name": "Helping Hobo Party"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party you are trying to update does not exist.",
    }


def test_party_delete(create_party, db_session):
    response = client.delete(f"/api/parties/{create_party.id}")
    cls = db_session.query(Party).filter(Party.id == create_party.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": "Party has been deleted."}
    assert cls == None


def test_party_delete(create_party, db_session):
    response = client.delete(f"/api/parties/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The party you are trying to delete does not exist."
    }
