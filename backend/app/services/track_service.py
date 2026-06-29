import uuid
from sqlalchemy.orm import Session
from app.models.track import Track
from app.repositories.track_repository import TrackRepository
from app.schemas.track import TrackCreate
from app.schemas.track import TrackOut
from app.repositories.track_repository import TrackRepository

class TrackService:
    def __init__(self, db: Session):
        self.track_repository = TrackRepository(db)

    def create_track(self, track_data: TrackCreate) -> TrackOut:
        new_track = Track(
            title=track_data.title,
            artist=track_data.artist,
            album=track_data.album,
            duration=track_data.duration,
            storage_url=track_data.storage_url,
            embedding=track_data.embedding,
            genre=track_data.genre,
            owner_id=track_data.owner_id
        )
        created_track = self.track_repository.create(new_track)
        return TrackOut.model_validate(created_track)
    
    def get_track_by_id(self, track_id: uuid.UUID) -> TrackOut | None:
        track = self.track_repository.get_by_id(track_id)
        if track:
            return TrackOut.model_validate(track)
        return None

    def get_track_by_title(self, title: str) -> TrackOut | None:
        track = self.track_repository.get_by_title(title)
        if track:
            return TrackOut.model_validate(track)
        return None