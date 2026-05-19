from sqlalchemy import String, Boolean, Integer, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from backend.app.models.base import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    
    password_analyses = relationship("PasswordAnalyzed", back_populates="user")
    