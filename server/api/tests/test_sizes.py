from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_sizes(create_size, db_session):
    response = client.get("/api/sizes")
    assert response.status_code == 200
    assert response.json() == {
        "sizes": [
            {"name": "Tiny", "id": 1},
        ]
    }


def test_get_no_sizes(db_session):
    response = client.get("/api/sizes")
    assert response.status_code == 404
    assert response.json() == {"detail": "No sizes found."}


def test_get_size(create_size, db_session):
    response = client.get("/api/sizes/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Tiny", "creatures": [], "races": []}


def test_get_no_size(create_size, db_session):
    response = client.get("/api/sizes/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Size not found."}
