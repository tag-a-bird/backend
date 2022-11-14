from os import getenv, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = getenv('FLASK_SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = getenv('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    LOGIN_DISABLED = False
    DATABASE_URI = getenv('FLASK_DATABASE_URI')


class TestConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = False
    TESTING = True
    LOGIN_DISABLED = True
    DATABASE_URI = getenv('FLASK_TEST_DATABASE_URI')
