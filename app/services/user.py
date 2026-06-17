from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        user = UserService.get_user_by_email(db, user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email này đã được đăng ký."
            )
        
        db_user = User(
            email=user_in.email,
            full_name=user_in.full_name or "New User",
            password_hash=hash_password(user_in.password),
            phone=user_in.phone_number
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User | None:
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def update_profile(db: Session, db_user: User, full_name: Optional[str], phone: Optional[str], avatar_url: Optional[str]) -> User:
        if full_name is not None:
            db_user.full_name = full_name
        if phone is not None:
            db_user.phone = phone
        if avatar_url is not None:
            db_user.avatar_url = avatar_url
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def change_password(db: Session, db_user: User, old_password: str, new_password: str) -> None:
        if not verify_password(old_password, db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu hiện tại không chính xác."
            )
        db_user.password_hash = hash_password(new_password)
        db.commit()

