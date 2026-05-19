from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, Text, String, Integer, TIMESTAMP
from sqlalchemy.sql import func
from datetime import datetime

from backend.app.models.base import Base

class PasswordAnalyzed(Base):
    __tablename__ = "password_analyses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    security_score: Mapped[int] = mapped_column(Integer)
    security_status: Mapped[str] = mapped_column(String)
    vulnerabilities: Mapped[str] = mapped_column(Text, default="[]")
    feedback: Mapped[str] = mapped_column(Text, default="[]")
    analyzed_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    
    user = relationship("User", back_populates="password_analyses")