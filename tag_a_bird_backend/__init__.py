import os
from dotenv import load_dotenv
from flask import Flask
from flask_toastr import Toastr
from tag_a_bird_backend.database import init_engine, init_db

toastr = Toastr()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    load_dotenv()
    app.config.from_prefixed_env()

    # from . import db
    # db.init_app(app)

    init_engine(app.config['DATABASE_URI'])
    init_db()

    toastr.init_app(app)

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