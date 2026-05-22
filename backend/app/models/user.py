from sqlalchemy import String, Boolean, UUID, TIMESTAMP, Index
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from backend.app.models.base import Base

class User(Base):
    """Database model representing a registered user.

    Attributes:
        id: Unique identifier generated automatically as a UUID v4.
        username: Unique username used for login and identification.
        email: Unique email address of the user.
        password_hash: Bcrypt-hashed version of the user's password. The plain text password is never stored.
        is_active: Indicates whether the account is active. Defaults to True on creation.
        created_at: Timestamp of account creation. Set automatically by the database server.
        modified_at: Timestamp of the last update. Updated automatically by the database server on every change.
    """
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4,)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    #password_analysis= relationship("PasswordSecurityAnalysis", back_populates="user")
    
    __table_args__ = (
        Index("users_email_key", "email")
    )