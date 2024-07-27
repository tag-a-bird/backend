from flask import Flask
from flask_toastr import Toastr
from flask_login import LoginManager
from flask_migrate import Migrate
from .db import configure_engine, db_session, engine, Base
from . import config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from secure import Secure
from os import getenv
import sentry_sdk



secure_headers = Secure()

toastr = Toastr()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address, headers_enabled=True)
migrate = Migrate()

def create_app(config_object=None):

    sentry_sdk.init(
    dsn=getenv("FLASK_SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    )
    
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        config_type = getenv('FLASK_CONFIG_TYPE')
        if config_type == 'production':
            app.config.from_object(config.ProdConfig)
        else:
            app.config.from_object(config.DevConfig)
    
    configure_engine(app.config['DATABASE_URI'])

    from .models import Base
    Base.metadata.create_all(bind=engine)

    # Register blueprints
    from .blueprints.auth.routes import auth_bp
    from .blueprints.admin.routes import admin_bp
    from .blueprints.annotation.routes import annotation_bp
    from .blueprints.general.routes import general_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(annotation_bp)
    app.register_blueprint(general_bp)

    toastr.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, Base)  # Initialize Flask-Migrate

    @app.after_request
    def set_secure_headers(response):
        secure_headers.framework.flask(response)
        return response

    with app.app_context():
        login_manager.init_app(app)

    return app