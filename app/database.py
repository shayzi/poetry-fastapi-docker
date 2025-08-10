from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from config import settings


engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,  # Set to False in production
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=300,  # Recycle connections every 5 minutes
)


def create_db_and_tables():
    """Create database tables from SQLModel metadata"""
    SQLModel.metadata.create_all(engine)


# Session factory
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session"""
    with LocalSession() as session:
        try:
            yield session
        finally:
            session.close()


def get_db_session() -> Session:
    """Get a database session for direct usage (scripts, etc.)"""
    return LocalSession()
