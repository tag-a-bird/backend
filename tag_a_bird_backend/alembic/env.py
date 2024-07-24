from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from flask import current_app
from tag_a_bird_backend import create_app
from tag_a_bird_backend.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    app = create_app()
    with app.app_context():
        url = current_app.config.get('DATABASE_URI')
        if not url:
            raise EnvironmentError("DATABASE_URI environment variable not set in Flask config")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    app = create_app()
    with app.app_context():
        url = current_app.config.get('DATABASE_URI')
        if not url:
            raise EnvironmentError("DATABASE_URI environment variable not set in Flask config")

        from tag_a_bird_backend.db import configure_engine, get_engine

        configure_engine(url)
        connectable = get_engine()

        if not connectable:
            raise RuntimeError("Database engine is not configured correctly")

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()