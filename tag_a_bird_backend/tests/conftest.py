import pytest
import datetime
import uuid
from tag_a_bird_backend.utils import config
from tag_a_bird_backend.main import create_app
from tag_a_bird_backend.utils.models import User, Annotation, QueryConfig, Record
from flask_login import FlaskLoginClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tag_a_bird_backend.utils.db import Base

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(config.TestConfig)
    app.test_client_class = FlaskLoginClient

    yield app

@pytest.fixture
def test_client(app):
    yield app.test_client()
    
@pytest.fixture
def test_user():
    user = User(
                id  = uuid.uuid4(),
                username = 'testuser',
                email = 'test@email.com',
                created_on = datetime.datetime.now()
                )
    user.set_password('testpassword')
    return user

@pytest.fixture
def setup_test_database(app):
    engine = create_engine(app.config['DATABASE_URI'])
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def test_query_config(setup_test_database):
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

@pytest.fixture
def test_annotation(setup_test_database):
    test_session = setup_test_database
    test_session.add(
        User(
            id  = '2e3317a6-920c-42b9-a3c3-797422ac0b41',
            username = 'fakeuser',
            email = 'fake@email.com',
            salt = b'fakesalt',
            password_hash = b'fakehash',
            created_on = '2022-12-06 12:34:36.019047'
        ))
    test_session.add(
        Record(
            id = 9811488,
            created_at = '2022-12-06 12:34:36.019047',
            audio_url = 'placeholder',
            photo_url = 'placeholder',
            comment = 'placeholder',
            country = 'placeholder',
            city = 'placeholder',
            habitat = 'placeholder',
            species = 'placeholder',
            weather = 'placeholder',
            date = '2022-12-06 12:34:36.019047',
            device_os = 'placeholder',
            is_holiday = False,
            human_noise = True,
            device_model = 'placeholder',
            habitat_other = 'placeholder',
            species_other = 'placeholder',
            day_of_the_week = 'placeholder',
            human_noise_type = 'placeholder',
            location_private = True,
            location_accuracy = 'placeholder',
            dawn_chorus_import_id = 'placeholder',
            human_noise_intensity = 'placeholder',
            organization_membership = 'placeholder',
            advanced_audio_equipment = 'placeholder',
            status = 'placeholder'
        ))
    test_session.add(
        Annotation(
            id = 3,
            recording_id = 9811488,
            user_id = "2e3317a6-920c-42b9-a3c3-797422ac0b41",
            start_time = 10,
            end_time = 20,
            label = "{Mönchsgrasmücke,Haussperling}",
            status = "{}"
        ))
    test_session.commit()
    yield test_session
    test_session.query(Annotation).delete()
    test_session.commit()
    test_session.query(Record).delete()
    test_session.commit()
    test_session.query(User).delete()
    test_session.commit()
