import uuid
from pydantic import BaseModel, ConfigDict


class TrackCreate(BaseModel):
    title: str
    artist: str
    album: str | None = None
    cover_url: str | None = None  # URL to the cover image
    duration: float  # Duration in seconds
    storage_url: str  # URL to the stored audio file
    genre: str | None = None
    source: str = "local"  # Source of the track, default is "local"

class TrackOut(BaseModel):
    id: uuid.UUID
    title: str
    artist: str
    album: str | None
    owner_id: uuid.UUID
    cover_url: str | None
    duration: float
    storage_url: str
    genre: str | None
    model_config = ConfigDict(from_attributes=True)
