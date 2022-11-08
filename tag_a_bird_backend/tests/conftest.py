import os
import tempfile
import pytest
from tag_a_bird_backend import config, create_app
from tag_a_bird_backend.db import Base, db_session
from flask_login import FlaskLoginClient

# read in SQL for populating test data
# with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
#     _data_sql = f.read().decode("utf8")

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app(config.TestConfig)
    app.test_client_class = FlaskLoginClient

    # create the database and load test data

    yield app

    # close and remove the temporary database

@pytest.fixture
def client(app):
    yield app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

