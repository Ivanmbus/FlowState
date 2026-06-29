# app/schemas/user.py
import uuid
from pydantic import BaseModel, EmailStr


#Los esquemas pydantic permiten validar y serializar datos de entrada y salida para la API.

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = None

class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    display_name: str | None
    mode: str
    profile_picture_url: str | None

    class Config:
        from_attributes = True  