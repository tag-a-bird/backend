import base64
import datetime
import uuid
import pytest
from flask import g, session
from tag_a_bird_backend.models import User
# from tag_a_bird_backend.tests.conftest import app

def test_user_password_hashing():
    user = User(
                    id  = uuid.uuid4(),
                    username = 'testuser',
                    email = 'test@email.com',
                    created_on = datetime.datetime.now()
                    )
    user.set_password('testpassword')
    assert user.verify_password('testpassword')

# def test_request_with_logged_in_user(app):
#     user = User.query.get[('b40ecc45-3f4b-4be6-872f-d1c6cb2e7b49')]
#     with app.test_client(user=user) as client:
#         # This request has user 1 already logged in!
#         client.get("/")

def test_register_function(client, app):
    pass
    # response = client.post(
    #     '/api/register', data={'username': 'a', 'password': 'a'}
    # )
    # assert response.headers["Location"] == "/api/login"

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

