"""
SQLAlchemy database models.
"""
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

try:
    from ..config.database import Base
except ImportError:
    from config.database import Base


class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Profile information
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    state = Column(String(100), nullable=True)
    occupation = Column(String(100), nullable=True)
    income = Column(Float, nullable=True)
    category = Column(String(50), nullable=True)

    # Eligibility flags
    disability = Column(Boolean, default=False)
    student_status = Column(Boolean, default=False)
    farmer_status = Column(Boolean, default=False)

    # Profile assets
    profile_photo_path = Column(String(1000), nullable=True)
    profile_photo_updated_at = Column(DateTime, nullable=True)


class Favorite(Base):
    """Favorite schemes model for tracking user favorites."""
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    scheme_id = Column(String(500), nullable=False)
    scheme_name = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Unique constraint: user can only favorite a scheme once
    __table_args__ = (UniqueConstraint("user_id", "scheme_id", name="uq_user_scheme"),)


class Reminder(Base):
    """Reminder model for user deadlines and custom events."""

    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    reminder_date = Column(DateTime, nullable=False, index=True)
    related_scheme_name = Column(String(500), nullable=True)
    reminder_type = Column(String(50), nullable=False, default="custom")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_reminders_user_date", "user_id", "reminder_date"),
    )


class UserDocument(Base):
    """User-uploaded documents metadata model."""

    __tablename__ = "user_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    document_type = Column(String(100), nullable=False)
    original_name = Column(String(500), nullable=False)
    stored_name = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False, default=0)
    relative_path = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_user_documents_user_created", "user_id", "created_at"),
    )
