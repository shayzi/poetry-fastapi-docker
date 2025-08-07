import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Add the app directory to the Python path
app_dir = Path(__file__).parent.parent / "app"
sys.path.append(str(app_dir))

# Import SQLModel and models
from sqlmodel import SQLModel

# Import all models to ensure they're registered with SQLModel metadata
from models.item import Item  # noqa: F401
# Import any additional models here as you create them

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate' support
target_metadata = SQLModel.metadata


def get_database_url() -> str:
    """Get database URL from environment variables"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Fallback for local development
        database_url = "postgresql://dbuser:dbpassword@localhost:5432/homeassignment"
    return database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
        user_module_prefix="sqlmodel.sql.sqltypes.",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Set the database URL in the configuration
    database_url = get_database_url()
    config.set_main_option("sqlalchemy.url", database_url)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # Important for SQLite compatibility
            user_module_prefix="sqlmodel.sql.sqltypes.",  # SQLModel types
            compare_type=True,  # Detect column type changes
            compare_server_default=True,  # Detect default value changes
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()