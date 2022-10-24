import os
from dotenv import load_dotenv
from flask import Flask
from .models import Base

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    load_dotenv()

    app.config.from_prefixed_env()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
