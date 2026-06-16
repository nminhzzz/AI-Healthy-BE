import sys
import os

# Ensure the backend directory is in the python path BEFORE importing 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.mysql import SessionLocal
from app.services.user import UserService
from app.schemas.user import UserCreate
from app.models.user import UserRole
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_admin():
    db = SessionLocal()
    try:
        user_in = UserCreate(email="admin@gmail.com", password="123456", full_name="System Admin")
        # Tạo user thường
        user = UserService.create_user(db, user_in)
        # Nâng cấp lên quyền ADMIN
        user.role = UserRole.ADMIN
        db.commit()
        print("Admin user admin@gmail.com created successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
