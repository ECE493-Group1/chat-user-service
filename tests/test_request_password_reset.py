import pytest

def test_request_password_reset_successful(client, app, session, auth):
    resp = auth.register()
    assert resp.status_code == 200

    body = {
        "email": auth.email
    }
    resp = client.post("/request-password-reset", json=body)

    assert resp.status_code == 200

    assert resp.json["message"] == "password reset link sent"


def test_request_password_reset_email_missing(client, app, session, auth):
    resp = auth.register()
    assert resp.status_code == 200

    body = {
        "email": ''
    }
    resp = client.post("/request-password-reset", json=body)

    assert resp.status_code == 400

    assert resp.json["message"] == "email missing"