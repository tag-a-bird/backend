import pytest
import datetime
import uuid
from tag_a_bird_backend import config, create_app
from tag_a_bird_backend.models import User, Annotation, QueryConfig
from flask_login import FlaskLoginClient
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from tag_a_bird_backend.db import Base

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

@pytest.fixture()
def new_user():
    user = User(
                id  = uuid.uuid4(),
                username = 'testuser',
                email = 'test@email.com',
                created_on = datetime.datetime.now()
                )
    user.set_password('testpassword')
    return user

@pytest.fixture(scope='function')
def setup_test_database(app):
    engine = create_engine(app.config['DATABASE_URI'])
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope='function')
def test_data(setup_test_database):
    test_session = setup_test_database
    test_session.add_all([
        QueryConfig(parameter='country', value ='Hungary'),
        QueryConfig(parameter='with_annotation', value='False'),
        QueryConfig(parameter='in_status', value=''),
        QueryConfig(parameter='not_in_status', value='')
        ])
    test_session.commit()
    yield test_session
    test_session.query(QueryConfig).delete()
    test_session.commit()
