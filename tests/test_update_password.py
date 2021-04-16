import pytest

# def test_update_password_missing_reset_token(client, app, session, auth):
#     resp = auth.register()
#     assert resp.status_code == 200

#     body = {
#         "reset_token": '',
#         "new_password": "newpassword123"
#     }
#     resp = client.post("/update-password", json=body)

#     assert resp.status_code == 400

#     assert resp.json["message"] == "reset token or new password missing"

# def test_update_password_invalid_token(client, app, session, auth):
#     resp = auth.register()
#     assert resp.status_code == 200

#     body = {
#         "reset_token": 'invalidtoken',
#         "new_password": "newpassword123"
#     }
#     resp = client.post("/update-password", json=body)

#     assert resp.status_code == 400

#     assert resp.json["message"] == "invalid token"