from sqlalchemy import String, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID, ENUM as PG_ENUM, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, List
import uuid

from backend.app.models.base import Base
from backend.app.models.user import User
from backend.app.schemas import SecurityStatus

class PasswordSecurityAnalysis(Base):
    __tablename__ = "password_security_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # CHAR(64) exacto para hashes SHA-256
    password_hash: Mapped[str] = mapped_column(
        String, 
    )
    
    security_status: Mapped[SecurityStatus] = mapped_column(
        PG_ENUM(
            SecurityStatus,
            name="password_status_enum",
            create_type=False,
        )
    )
    
    details: Mapped[Dict[str, List[str]]] = mapped_column(
        JSONB, 
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    __table_args__ = (
        Index("idx_pwd_analyses_hash", "password_hash"),
        Index("idx_pwd_analyses_details_gin", "details", postgresql_using="gin"),
    )
    
    user: Mapped["User"] = relationship(back_populates="password_analysis")