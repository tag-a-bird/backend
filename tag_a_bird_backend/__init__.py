from datetime import timedelta
from flask import Flask, session, g
from flask_toastr import Toastr
from flask_login import LoginManager, current_user
from . import config
from .db import configure_engine
from alembic import config as alembic_config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from secure import Secure

secure_headers = Secure()
toastr = Toastr()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address, headers_enabled=True)

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        session.modified = True
        g.user = current_user

    @app.after_request
    def set_secure_headers(response):
        secure_headers.framework.flask(response)
        return response

    toastr.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        login_manager.init_app(app)
        if app.config != config.TestConfig:
            configure_engine(app.config['DATABASE_URI'])

        from tag_a_bird_backend.routes import route_blueprint
        app.register_blueprint(route_blueprint)

    return app