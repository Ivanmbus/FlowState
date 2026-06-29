import uuid
from pydantic import BaseModel, ConfigDict


class TrackCreate(BaseModel):
    title: str
    artist: str
    album: str | None = None
    duration: float  # Duration in seconds
    storage_url: str  # URL to the stored audio file
    genre: str | None = None

class TrackOut(BaseModel):
    id: uuid.UUID
    title: str
    artist: str
    album: str | None
    duration: float
    storage_url: str
    genre: str | None
    model_config = ConfigDict(from_attributes=True)

    class Config:
        from_attributes = True