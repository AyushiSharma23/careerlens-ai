"""Database connection setup (SQLite through SQLAlchemy)."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# The database location can be changed with an environment variable later.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./careerlens.db")

# check_same_thread=False is needed because FastAPI may use SQLite from several threads.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Parent class of all database table classes."""


def get_db():
    """Give each request its own database session and close it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()