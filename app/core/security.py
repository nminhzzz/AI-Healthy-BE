"""
core/security.py — Xử lý bảo mật: password hashing và JWT token.

Functions:
    hash_password(plain)        → bcrypt hash
    verify_password(plain, hash)→ bool
    create_access_token(data)   → JWT access token (30 phút)
    create_refresh_token(data)  → JWT refresh token (7 ngày)
    decode_token(token)         → payload dict | None
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
import bcrypt

from app.core.config import settings

# ── Password hashing ──────────────────────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Hash mật khẩu bằng bcrypt trước khi lưu DB."""
    pwd_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So sánh mật khẩu người dùng nhập với hash trong DB."""
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_bytes)


# ── JWT helpers ───────────────────────────────────────────────────────────────

def _create_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    """Tạo JWT token nội bộ."""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(data: dict[str, Any]) -> str:
    """
    Tạo JWT Access Token (ngắn hạn).
    Mặc định hết hạn sau ACCESS_TOKEN_EXPIRE_MINUTES phút.

    Args:
        data: Payload muốn encode. Thường chứa {"sub": str(user_id), "role": role}.

    Returns:
        JWT token string.
    """
    return _create_token(
        data={**data, "type": "access"},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(data: dict[str, Any]) -> str:
    """
    Tạo JWT Refresh Token (dài hạn).
    Mặc định hết hạn sau REFRESH_TOKEN_EXPIRE_DAYS ngày.

    Args:
        data: Payload — thường chỉ cần {"sub": str(user_id)}.

    Returns:
        JWT token string.
    """
    return _create_token(
        data={**data, "type": "refresh"},
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict[str, Any] | None:
    """
    Giải mã và xác thực JWT token.

    Args:
        token: JWT token string từ Authorization header.

    Returns:
        Payload dict nếu hợp lệ, None nếu token sai / hết hạn.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        return None
