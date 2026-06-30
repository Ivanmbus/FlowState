import uuid
from sqlalchemy.orm import Session
from app.models.track import Track
from app.repositories.track_repository import TrackRepository
from app.schemas.track import TrackCreate
from app.schemas.track import TrackOut
from backend.app.repositories.user_repository import UserRepository

class TrackService:
    def __init__(self, db: Session):
        self.track_repository = TrackRepository(db)
        self.user_repository = UserRepository(db)

    def create_track(self, track_data: TrackCreate, owner_id: uuid.UUID) -> TrackOut:
        owner = self.user_repository.get_by_id(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        if owner.mode == "public" and track_data.source != "local":
            raise ValueError("Public users can only create tracks with source 'local'")

        new_track = Track(
            title=track_data.title,
            artist=track_data.artist,
            album=track_data.album,
            duration=track_data.duration,
            storage_url=track_data.storage_url,
            genre=track_data.genre,
            owner_id=owner_id,
            source=track_data.source
        )
        created_track = self.track_repository.create(new_track)
        return TrackOut.model_validate(created_track)
    
    def get_track_by_id(self, track_id: uuid.UUID) -> TrackOut | None:
        track = self.track_repository.get_by_id(track_id)
        if track:
            return TrackOut.model_validate(track)
        return None

    def get_track_by_title(self, title: str) -> list[TrackOut] | None:
        tracks = self.track_repository.get_by_title(title)
        if tracks:
            return [TrackOut.model_validate(track) for track in tracks]
        return None
    
    def get_all_tracks(self) -> list[TrackOut]:
        tracks = self.track_repository.get_all_tracks()
        return [TrackOut.model_validate(track) for track in tracks]