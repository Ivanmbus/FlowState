from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = service.create_token_for_user(user)
    return TokenResponse(access_token=token)