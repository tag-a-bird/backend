from flask import Flask
from flask_toastr import Toastr
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from .db import Base, configure_engine, db_session

auth = HTTPBasicAuth()
toastr = Toastr()
login_manager = LoginManager()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    configure_engine(app.config['DATABASE_URI']) 
    Base.query = db_session.query_property()

    from tag_a_bird_backend.routes import route_blueprint
    app.register_blueprint(route_blueprint)

    toastr.init_app(app)

    with app.app_context():
        login_manager.init_app(app)

    return app