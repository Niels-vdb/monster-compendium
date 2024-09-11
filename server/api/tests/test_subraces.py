from fastapi.testclient import TestClient

from .conftest import app


client = TestClient(app)


def test_get_subraces(create_subrace, db_session):
    response = client.get("/api/subraces")
    assert response.status_code == 200
    assert response.json() == {
        "subraces": [
            {"name": "Duergar", "race_id": 1, "id": 1},
        ]
    }


def test_get_no_subraces(db_session):
    response = client.get("/api/subraces")
    assert response.status_code == 404
    assert response.json() == {"detail": "No subraces found."}


def test_get_subrace(create_subrace, db_session):
    response = client.get("/api/subraces/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Duergar",
        "race": {"id": 1, "name": "Dwarf", "size_id": 1},
        "resistances": [],
    }


def test_get_no_subrace(create_subrace, db_session):
    response = client.get("/api/subraces/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Subrace not found."}
