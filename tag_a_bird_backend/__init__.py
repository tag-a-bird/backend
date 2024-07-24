from flask import Flask
from flask_toastr import Toastr
from flask_login import LoginManager
from flask_migrate import Migrate
from .db import configure_engine, db_session, engine, Base
from . import config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from secure import Secure

secure_headers = Secure()

toastr = Toastr()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address, headers_enabled=True)
migrate = Migrate()

def create_app():
    app = Flask(__name__)
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