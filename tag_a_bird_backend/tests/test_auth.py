import base64
import pytest
from flask import g, session

# from tag_a_bird_backend import app
# from flaskr.db import get_db

def test_admin(client):
    # assert client.get('/api/admin').status_code == 401
    resp = client.get('/api/admin')
    assert resp.status == '401 UNAUTHORIZED'

# def test_register(client, app):
#     assert client.get('/api/signup').status_code == 200
    # response = client.post(
    #     '/api/signup', data={'username': 'a', 'password': 'a'}
    # )
    # assert response.headers["Location"] == "/api/signin"

    # with app.app_context():
    #     assert get_db().execute(
    #         "SELECT * FROM user WHERE username = 'a'",
    #     ).fetchone() is not None


# @pytest.mark.parametrize(('username', 'password', 'message'), (
#     ('', '', b'Username is required.'),
#     ('a', '', b'Password is required.'),
#     ('test', 'test', b'already registered'),
# ))
# def test_register_validate_input(client, username, password, message):
#     response = client.post(
#         '/auth/register',
#         data={'username': username, 'password': password}
#     )
#     assert message in response.data


# def test_admin_unauth():
#     web = app.test_client()

#     rv = web.get('/api/admin')
#     assert rv.status == '401 UNAUTHORIZED'
#     assert rv.data == b'Unauthorized Access'
#     assert 'WWW-Authenticate' in rv.headers
#     assert rv.headers['WWW-Authenticate'] == 'Basic realm="Authentication Required"'

# def test_admin_auth():
#     web = app.test_client()

#     credentials = base64.b64encode(b'kinga:test').decode('utf-8')
#     rv = web.get('/api/admin', headers={
#             'Authorization': 'Basic ' + credentials
#     })

#     assert rv.status == '200 OK'
#     assert rv.data == b'hello admin'
