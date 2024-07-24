import os
from flask_migrate import upgrade, migrate, init
from tag_a_bird_backend import create_app
from tag_a_bird_backend.db import db_session

app = create_app()
app.app_context().push()

def run_migrations():
    if not os.path.exists('migrations'):
        init()

    migrate(message="Auto-migrate")
    upgrade()

if __name__ == "__main__":
    run_migrations()