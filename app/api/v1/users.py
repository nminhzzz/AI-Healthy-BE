from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, PasswordChange
from app.services.user import UserService

router = APIRouter()

@router.put("/profile", response_model=UserResponse)
def update_profile(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cập nhật thông tin cá nhân (Họ tên, SĐT, Avatar) của người dùng hiện tại.
    """
    return UserService.update_profile(
        db, 
        db_user=current_user, 
        full_name=user_in.full_name, 
        phone=user_in.phone, 
        avatar_url=user_in.avatar_url
    )


@router.put("/password", status_code=status.HTTP_200_OK)
def change_password(
    pwd_in: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Thay đổi mật khẩu của người dùng hiện tại.
    """
    UserService.change_password(
        db, 
        db_user=current_user, 
        old_password=pwd_in.old_password, 
        new_password=pwd_in.new_password
    )
    return {"message": "Thay đổi mật khẩu thành công."}
