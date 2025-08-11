from typing import Generator

from sqlmodel import Session, create_engine as create_sqlmodel_engine

from config import settings


engine = create_sqlmodel_engine(
    settings.database_url,
    echo=settings.database_echo,  # Set to False in production
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=300,  # Recycle connections every 5 minutes
)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session"""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
