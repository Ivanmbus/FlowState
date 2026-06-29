import uuid
from sqlalchemy.orm import Session
from app.models.user import User

class TrackRepository: 
    def __init__(self, db:Session):
        self.db = db

    def get_by_id(self, track_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == track_id).first()
    
    def get_by_title(self, title: str) -> User | None:
        return self.db.query(User).filter(User.title == title).first()
    
    def create(self, track: User) -> User:
        self.db.add(track)
        self.db.commit()
        self.db.refresh(track)
        return track
    
