from tag_a_bird_backend.utils import config
from os import getenv

from tag_a_bird_backend.main import create_app

# def test_config():
#     assert create_app(config.TestConfig).testing

def test_prod_config(app):
    app.config.from_object(config.ProdConfig)
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['DATABASE_URI'] == getenv('PROD_DATABASE_URI')

def test_dev_config(app):
    app.config.from_object(config.DevConfig)
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['DATABASE_URI'] == getenv('FLASK_DATABASE_URI')

def test_test_config(app):
    app.config.from_object(config.TestConfig)
    assert not app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['LOGIN_DISABLED']
    assert app.config['DATABASE_URI'] == getenv('FLASK_TEST_DATABASE_URI')
