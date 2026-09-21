"""
Database configuration and session management.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

try:
    from .settings import DATABASE_URL
except ImportError:
    from config.settings import DATABASE_URL

# Database connection setup
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def _ensure_sqlite_additive_columns() -> None:
    """Apply additive SQLite column updates for backward compatibility."""
    if not DATABASE_URL.startswith("sqlite"):
        return

    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(users)")).fetchall()
        existing_columns = {row[1] for row in rows}

        if "profile_photo_path" not in existing_columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN profile_photo_path VARCHAR(1000)"))

        if "profile_photo_updated_at" not in existing_columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN profile_photo_updated_at DATETIME"))


def init_database() -> None:
    """Import models and create all database tables."""
    try:
        from ..models import database as _models  # noqa: F401
    except ImportError:
        from models import database as _models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_additive_columns()
