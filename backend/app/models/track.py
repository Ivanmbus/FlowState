import uuid
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    album = Column(String(255), nullable=True)
    duration = Column(Float, nullable=False)  # Duration in seconds
    storage_url = Column(String(255), nullable=False)  # URL to the stored audio file
    embedding = Column(Vector(1536), nullable=True)  # Vector representation of the audio
    genre = Column(String(100), nullable=True)

    owner = relationship("User", back_populates="tracks")
    
