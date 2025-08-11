from typing import Generator

from sqlmodel import Session, SQLModel
from sqlmodel import create_engine as sqlmodel_create_engine

from config import settings


engine = sqlmodel_create_engine(
    settings.database_url,
    echo=settings.database_echo,  # Set to False in production
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=300,  # Recycle connections every 5 minutes
)


def create_db_and_tables():
    """Create database tables from SQLModel metadata"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session"""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def get_db_session() -> Session:
    """Get a database session for direct usage (scripts, etc.)"""
    return Session(engine)
