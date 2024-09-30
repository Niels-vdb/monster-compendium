from fastapi.testclient import TestClient

from .conftest import app

client = TestClient(app)


def test_login_user(create_user, db_session):
    response = client.post(
        "/login/",
        json={"username": "Test", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Your logged in with valid credentials. Welcome."
    }
    assert response.cookies["user_id"] == str(create_user.id)


def test_login_wrong_user(create_user, db_session):
    response = client.post(
        "/login/",
        json={"username": "Test2", "password": "password"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The username you try to log in with does not exist."
    }


def test_login_wrong_password(create_user, db_session):
    response = client.post(
        "/login/",
        json={"username": "Test", "password": "password1"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The password you try to log in with is incorrect."
    }
