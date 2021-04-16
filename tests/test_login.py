import pytest

from app.models import Users

def test_successful_login(client, app, session, auth):
    resp = auth.register()
    assert resp.status_code == 200

    body = {
        "email": auth.email,
        "password": auth.password
    }
    resp = client.post("/login", json=body)

    assert resp.status_code == 200

    assert resp.json["token"] is not None


def test_login_missing_email(client, app, session, auth):
    resp = auth.register()
    assert resp.status_code == 200

    body = {
        "email": '',
        "password": auth.password
    }
    resp = client.post("/login", json=body)

    assert resp.status_code == 400

    assert resp.json["message"] == "email or password missing"


def test_login_incorrect_password(client, app, session, auth):
    resp = auth.register()
    assert resp.status_code == 200

    password = "abcdefg"
    assert password != auth.password

    body = {
        "email": auth.email,
        "password": password
    }
    resp = client.post("/login", json=body)

    assert resp.status_code == 400

    assert resp.json["message"] == "invalid password"