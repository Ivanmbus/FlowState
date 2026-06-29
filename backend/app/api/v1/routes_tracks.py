import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.track import TrackCreate, TrackOut
from app.services.track_service import TrackService

router = APIRouter(prefix= "/tracks", tags=["tracks"])

@router.post("/", response_model=TrackOut, status_code=201)
def create_track(data: TrackCreate, db: Session = Depends(get_db)):
    service = TrackService(db)
    try:
        track = service.create_track(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return track