import pytest

from app.models import Users

# def test_successful_registration(client, app, session):
#     test_email = "testuser@email.com"
#     test_username = "testuser"
#     test_password = "password123"
#     body = {
#         "email": test_email,
#         "username": test_username,
#         "password": test_password
#     }
#     resp = client.post("/register", json=body)

#     assert resp.status_code == 200

#     assert session.query(Users).filter_by(email=test_email).one_or_none()


# def test_missing_password(client, app, session):
#     test_email = "testuser@email.com"
#     test_username = "testuser"
#     body = {
#         "email": test_email,
#         "username": test_username,
#         "password": ""
#     }
#     resp = client.post("/register", json=body)

#     assert resp.status_code == 400

#     assert resp.json["message"] == "email, username or password missing"

# def test_username_four_chars_or_less(client, app, session):
#     test_email = "testuser@email.com"
#     test_username = "abc"
#     test_password = "password123"
#     body = {
#         "email": test_email,
#         "username": test_username,
#         "password": test_password,
#     }
#     resp = client.post("/register", json=body)

#     assert resp.status_code == 400

#     assert resp.json["message"] == "username must be 4 characters or more"


# def test_username_already_exists(client, app, session):
#     test_email1 = "testuser@email.com"
#     test_username1 = "testuser"
#     test_password1 = "password123"
#     body1 = {
#         "email": test_email1,
#         "username": test_username1,
#         "password": test_password1,
#     }
#     resp = client.post("/register", json=body1)

#     test_email2 = "testuser2@email.com"
#     test_username2 = "testuser"
#     test_password2 = "password12345"
#     body2 = {
#         "email": test_email2,
#         "username": test_username2,
#         "password": test_password2,
#     }
#     resp = client.post("/register", json=body2)

#     assert resp.status_code == 400

#     assert resp.json["message"] == "username already in use"



# def test_successful_login(client, app, session, auth):
#     resp = auth.register()
#     assert resp.status_code == 200

#     body = {
#         "email": auth.email,
#         "password": auth.password
#     }
#     resp = client.post("/login", json=body)

#     assert resp.status_code == 200