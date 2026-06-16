from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in_data = obj_in.model_dump(by_alias=False)
        password = obj_in_data.pop("password")
        # Ensure role is converted to enum if it is a string
        if "role" in obj_in_data and isinstance(obj_in_data["role"], str):
            from app.models.user import UserRole
            obj_in_data["role"] = UserRole[obj_in_data["role"]]
        db_obj = User(
            **obj_in_data,
            password_hash=hash_password(password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_user(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        obj_data = db_obj.__dict__
        update_data = obj_in.model_dump(exclude_unset=True, by_alias=False)
        if "password" in update_data and update_data["password"]:
            password = update_data.pop("password")
            db_obj.password_hash = hash_password(password)
        if "role" in update_data and isinstance(update_data["role"], str):
            from app.models.user import UserRole
            update_data["role"] = UserRole[update_data["role"]]
        for field in list(update_data.keys()):
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repo = UserRepository(User)
