from fastapi.testclient import TestClient

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
