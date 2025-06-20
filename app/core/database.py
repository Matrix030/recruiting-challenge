"""Database connection and session management.

This module handles SQLModel database setup and provides session management
utilities.
"""

from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import SQLITE_URL
from app.models.profile import Profile  # Import Profile model explicitly

# Create SQLite engine
engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

def create_db_and_tables() -> None:
    """Create all database tables."""
    # Drop all tables first to ensure clean state
    SQLModel.metadata.drop_all(engine)
    # Create tables with updated schema
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Get a database session.
    
    Yields:
        SQLModel session that will be automatically closed
    """
    with Session(engine) as session:
        yield session

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Context manager for database sessions.
    
    This is useful for scripts and tests that need explicit session management.
    
    Yields:
        SQLModel session that will be automatically closed
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close() 