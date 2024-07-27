from os import getenv, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = getenv('FLASK_SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    SECRET_KEY = getenv("FLASK_SECRET_KEY")
    DATABASE_URI = getenv('FLASK_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI 



class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = True
    TESTING = False



class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    LOGIN_DISABLED = False


class TestConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = False
    TESTING = True
    LOGIN_DISABLED = True
