from .conftest import client


def test_login(create_user):
    form_data = {
        "username": "test",
        "password": "password"
    }

    response = client.post("/token", data=form_data)
    assert response.status_code == 200
    assert response.json() == {'message': 'Your logged in with valid credentials. Welcome.'}


def test_incorrect_login(db_session):
    form_data = {
        "username": "test",
        "password": "password"
    }

    response = client.post("/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_not_authorized(db_session):
    response = client.get("/api/attributes/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
