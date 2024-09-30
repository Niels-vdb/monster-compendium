from fastapi.testclient import TestClient

from .conftest import app

client = TestClient(app)


def test_logout_user(create_user, db_session):
    response = client.delete("/logout/1")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Your logged out of the application. Goodbye."
    }


def test_logout_wrong_user(create_user, db_session):
    response = client.delete("/logout/4")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The id you try to log out with does not exist."
    }
