import pytest
from tag_a_bird_backend import app as flask_app

@pytest.fixture
def app():
    yield flask_app
@pytest.fixture
def client(app):
    return app.test_client()