import pytest

def test_user_search_successful(client, app, session, auth):
    test_email1 = "testuser@email.com"
    test_username1 = "testuser"
    test_password1 = "password123"
    resp = auth.register(test_email1, test_username1, test_password1)

    assert resp.status_code == 200

    test_email2 = "testuser2@email.com"
    test_username2 = "testuser2"
    test_password2 = "password123"
    resp = auth.register(test_email2, test_username2, test_password2)

    assert resp.status_code == 200

    test_email3 = "testuser3@email.com"
    test_username3 = "testuser3"
    test_password3 = "password123"
    resp = auth.register(test_email3, test_username3, test_password3)

    assert resp.status_code == 200

    resp = auth.login(test_email1, test_password1)

    assert resp.status_code == 200
    auth_token = resp.json["token"]

    headers = {"Authorization": "Bearer " + auth_token}
    body = {
        "search_query": "testuser"
    }
    resp = client.post("/user-search", json=body, headers=headers)

    assert resp.status_code == 200

    results = resp.json["results"]

    assert len(results) == 3
    assert test_username1 in results
    assert test_username2 in results
    assert test_username3 in results

def test_user_search_no_query(client, app, session, auth):
    test_email1 = "testuser@email.com"
    test_username1 = "testuser"
    test_password1 = "password123"
    resp = auth.register(test_email1, test_username1, test_password1)

    assert resp.status_code == 200

    resp = auth.login(test_email1, test_password1)

    assert resp.status_code == 200
    auth_token = resp.json["token"]

    headers = {"Authorization": "Bearer " + auth_token}
    body = {
        "search_query": ""
    }
    resp = client.post("/user-search", json=body, headers=headers)

    assert resp.status_code == 400
    assert resp.json["message"] == "no query provided"