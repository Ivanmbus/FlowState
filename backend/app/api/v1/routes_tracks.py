import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.track import TrackCreate, TrackOut
from app.services.track_service import TrackService
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix= "/tracks", tags=["tracks"])

@router.post("/", response_model=TrackOut, status_code=201)
def create_track(data: TrackCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TrackService(db)
    try:
        track = service.create_track(data, owner_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return track

@router.get("/{track_id}", response_model=TrackOut)
def get_track(track_id: uuid.UUID, db: Session = Depends(get_db)):
    service = TrackService(db)
    track = service.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

@router.get("/title/{title}", response_model=TrackOut)
def get_track_by_title(title: str, db: Session = Depends(get_db)):
    service = TrackService(db)
    track = service.get_track_by_title(title)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

