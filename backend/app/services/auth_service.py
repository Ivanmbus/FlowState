
from app.repositories.user_repository import UserRepository
from passlib.context import CryptContext
from app.core.security import create_access_token
from backend.app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db):
        self.user_repository = UserRepository(db)

    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.user_repository.get_by_email(email)
        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user

    def create_token_for_user(self, user: User) -> str:
        return create_access_token({"sub": str(user.id)})

