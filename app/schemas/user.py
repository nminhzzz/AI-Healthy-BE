from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = Field(None, alias="phone_number")
    avatar_url: Optional[str] = None

    class Config:
        populate_by_name = True
        from_attributes = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128, description="Mật khẩu phải từ 6-128 ký tự")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = Field(None, alias="phone_number")
    avatar_url: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

    class Config:
        populate_by_name = True
        from_attributes = True

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
