# app/services/user_service.py
import uuid
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, data: UserCreate) -> User:
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("El email ya está registrado")  # regla de negocio

        hashed = pwd_context.hash(data.password)
        new_user = User(
            email=data.email,
            password_hash=hashed,
            display_name=data.display_name,
            profile_picture_url=data.profile_picture_url,
        )
        return self.repo.create(new_user)

    def get_user(self, user_id: uuid.UUID) -> User | None:
        return self.repo.get_by_id(user_id)