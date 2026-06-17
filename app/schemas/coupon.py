from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CouponBase(BaseModel):
    code: str = Field(..., max_length=50, description="Mã giảm giá")
    discount_amount: float = Field(..., ge=0.0, description="Số tiền giảm giá (VND)")
    is_active: bool = Field(True, description="Trạng thái kích hoạt")
    expires_at: Optional[datetime] = Field(None, description="Ngày hết hạn")

class CouponCreate(CouponBase):
    pass

class CouponUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=50)
    discount_amount: Optional[float] = Field(None, ge=0.0)
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

class CouponResponse(CouponBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
