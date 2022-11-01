from flask import Flask
from flask_toastr import Toastr
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from .db import Base, configure_engine, engine
from . import config

auth = HTTPBasicAuth()
toastr = Toastr()
api = Api()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(config.DevConfig) # fix this later 

    from tag_a_bird_backend.routes import route_blueprint
    app.register_blueprint(route_blueprint)

    toastr.init_app(app)
    # api.init_app(app)

    with app.app_context():
        login_manager.init_app(app)

    configure_engine(app.config['DATABASE_URI'])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping()

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app