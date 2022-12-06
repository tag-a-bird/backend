from flask import Flask
from flask_toastr import Toastr
from flask_login import LoginManager
from . import config
from .db import configure_engine, db_session, engine
from .models import Base
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