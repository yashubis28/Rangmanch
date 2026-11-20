"""Database configuration and session dependency for the API."""

from sqlmodel import SQLModel, Session, create_engine


DATABASE_URL = "sqlite:///rangmanch.db"

# Keep SQL logging disabled during normal operation; enable echo temporarily while debugging.
engine = create_engine(DATABASE_URL, echo=False)


def create_tables() -> None:
    """Create every table declared by an SQLModel subclass."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency that provides a DB session per request."""
    with Session(engine) as session:
        yield session

