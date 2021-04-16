import pytest

# def test_verify_reset_token_missing_token(client, app, session, auth):
#     resp = auth.register()
#     assert resp.status_code == 200

#     body = {
#         "reset_token": ''
#     }
#     resp = client.post("/verify-reset-token", json=body)

#     assert resp.status_code == 400

#     assert resp.json["message"] == "reset token missing"

# def test_verify_reset_token_invalid_token(client, app, session, auth):
#     resp = auth.register()
#     assert resp.status_code == 200

#     body = {
#         "reset_token": 'invalidtoken'
#     }
#     resp = client.post("/verify-reset-token", json=body)

#     assert resp.status_code == 400

#     assert resp.json["message"] == "invalid token"