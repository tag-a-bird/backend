import os
from dotenv import load_dotenv
from flask import Flask
from flask_toastr import Toastr
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager

auth = HTTPBasicAuth()
toastr = Toastr()
api = Api()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from tag_a_bird_backend.app import route_blueprint
    app.register_blueprint(route_blueprint)

    load_dotenv()
    app.config.from_prefixed_env()

    toastr.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)

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