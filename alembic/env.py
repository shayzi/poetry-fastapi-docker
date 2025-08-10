from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from config import settings

# Import all models to ensure they're registered with SQLModel metadata
from models.item import Item  # noqa: F401

alembic_config = context.config

# Interpret the config file for Python logging. This line sets up loggers basically.
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata


def run_migrations() -> None:
    alembic_config.set_main_option("sqlalchemy.url", settings.database_url)

    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            user_module_prefix="sqlmodel.sql.sqltypes.",
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations()


# HOME_ASSIGNMENT_DATABASE_URL=postgresql://dbuser:dbpassword@localhost:5432/homeassignment
# poetry run alembic revision --autogenerate -m "XXX"