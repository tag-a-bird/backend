import pytest
import datetime
import uuid
from tag_a_bird_backend import config, create_app
from tag_a_bird_backend.models import User
from flask_login import FlaskLoginClient

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    app = create_app(config.TestConfig)
    app.test_client_class = FlaskLoginClient

    yield app

@pytest.fixture
def test_client(app):
    yield app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='module')
def new_user():
    user = User(
                    id  = uuid.uuid4(),
                    username = 'testuser',
                    email = 'test@email.com',
                    created_on = datetime.datetime.now()
                    )
    return user