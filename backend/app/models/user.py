# app/models/user.py
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    mode = Column(String(10), default="private")  # 'private' | 'public'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    profile_picture_url = Column(String(255), nullable=True)

    tracks = relationship("Track", back_populates="owner", cascade="all, delete-orphan")