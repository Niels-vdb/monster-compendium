from fastapi.testclient import TestClient

from server.database.models.characteristics import Size

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


def test_post_size(db_session):
    response = client.post(
        "/api/sizes",
        json={
            "size_name": "Medium",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "New size 'Medium' has been added to the database.",
        "size": {"id": 1, "name": "Medium"},
    }


def test_post_duplicate_size(db_session):
    client.post(
        "/api/sizes",
        json={
            "size_name": "Medium",
        },
    )
    response = client.post(
        "/api/sizes",
        json={
            "size_name": "Medium",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Size already exists."}


def test_size_name_put(create_size, db_session):
    response = client.put(
        f"/api/sizes/{create_size.id}",
        json={"size_name": "Medium"},
    )
    size = db_session.query(Size).first()
    assert response.status_code == 200
    assert size.name == "Medium"
    assert response.json() == {
        "message": "Size 'Medium' has been updated.",
        "size": {"id": 1, "name": "Medium"},
    }


def test_size_fake_size_put(create_race, create_size, db_session):
    response = client.put(
        "/api/sizes/2",
        json={"size_name": "Medium"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The size you are trying to update does not exist.",
    }


def test_size_delete(create_size, db_session):
    response = client.delete(f"/api/sizes/{create_size.id}")
    size = db_session.query(Size).filter(Size.id == create_size.id).first()
    assert response.status_code == 200
    assert response.json() == {"message": f"Size has been deleted."}
    assert size == None


def test_size_fake_delete(create_size, db_session):
    response = client.delete(f"/api/sizes/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The size you are trying to delete does not exist."
    }
