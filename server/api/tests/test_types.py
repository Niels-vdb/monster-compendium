from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_types(create_type, db_session):
    response = client.get("/api/types")
    assert response.status_code == 200
    assert response.json() == {
        "types": [
            {"name": "Aberration", "id": 1},
        ]
    }


def test_get_no_types(db_session):
    response = client.get("/api/types")
    assert response.status_code == 404
    assert response.json() == {"detail": "No types found."}


def test_get_type(create_type, db_session):
    response = client.get("/api/types/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Aberration", "creatures": []}


def test_get_no_type(create_type, db_session):
    response = client.get("/api/types/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Type not found."}
