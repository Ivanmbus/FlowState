import uuid
from sqlalchemy.orm import Session
from app.models.track import Track

class TrackRepository: 
    def __init__(self, db:Session):
        self.db = db

    def get_by_id(self, track_id: uuid.UUID) -> Track | None:
        return self.db.query(Track).filter(Track.id == track_id).first()
    
    def search_by_title(self, title: str) -> list[Track]:
        return self.db.query(Track).filter(Track.title.ilike(f"%{title}%")).all()

    def search_by_artist(self, artist: str) -> list[Track]:
        return self.db.query(Track).filter(Track.artist.ilike(f"%{artist}%")).all()

    def create(self, track: Track) -> Track:
        self.db.add(track)
        self.db.commit()
        self.db.refresh(track)
        return track
    
    def get_all_tracks(self) -> list[Track]:
        return self.db.query(Track).all()
    
    def get_by_owner(self, owner_id: uuid.UUID, limit: int = 50, offset: int = 0) -> list[Track]:
        return (
            self.db.query(Track)
            .filter(Track.owner_id == owner_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    def search_by_genre(self, genre: str) -> list[Track]:
        return self.db.query(Track).filter(Track.genre.ilike(f"%{genre}%")).all()
