from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, oauth2_scheme
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db.mysql import get_db
from app.db.redis import get_redis
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from redis.asyncio import Redis
from pydantic import BaseModel

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Đăng ký tài khoản người dùng mới.
    """
    user = UserService.create_user(db, user_in)
    return user

@router.post("/login", response_model=Token)
def login(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Đăng nhập bằng Email và Password lấy JWT Access Token.
    Refresh Token được tự động lưu vào HTTP-Only Cookie.
    """
    user = UserService.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản đã bị khóa.")
        
    # Tạo JWT token
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Gắn Refresh Token vào HTTP-Only Cookie (sống 7 ngày)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False, # Đổi thành True nếu chạy HTTPS trên server thật
        samesite="lax",
        path="/",
        max_age=7 * 24 * 60 * 60
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Lấy thông tin profile của người dùng đang đăng nhập.
    """
    return current_user

@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(
    response: Response,
    refresh_token: str | None = Cookie(None),
    db: Session = Depends(get_db)
) -> Any:
    """
    Tự động đọc Refresh Token từ Cookie để lấy Access Token mới.
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Không tìm thấy Refresh Token trong Cookie. Vui lòng đăng nhập lại.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token không hợp lệ hoặc đã hết hạn.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Người dùng không hợp lệ hoặc đã bị khóa.")
        
    new_access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Set lại cookie mới để xoay vòng token (Token Rotation)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
        max_age=7 * 24 * 60 * 60
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(
    response: Response,
    token: str = Depends(oauth2_scheme),
    redis_client: Redis = Depends(get_redis)
) -> Any:
    """
    Đăng xuất bằng cách xóa Cookie và đưa JWT hiện tại vào Blocklist trong Redis.
    """
    # 1. Xóa HttpOnly Cookie chứa Refresh Token
    response.delete_cookie(key="refresh_token", path="/")
    
    # 2. Block Access Token bằng Redis
    payload = decode_token(token)
    if payload:
        import time
        exp = payload.get("exp")
        now = int(time.time())
        ttl = exp - now
        if ttl > 0:
            # Lưu token vào Redis blocklist. Tự động xóa khỏi Redis khi token thật sự hết hạn
            await redis_client.setex(f"blocklist:{token}", ttl, "true")
            
    return {"message": "Đăng xuất thành công. Token đã bị vô hiệu hóa."}
