from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ShippingAddressBase(BaseModel):
    receiver_name: str = Field(..., max_length=255, description="Tên người nhận")
    phone: str = Field(..., max_length=20, description="Số điện thoại")
    province: str = Field(..., max_length=255, description="Tỉnh/Thành phố")
    district: str = Field(..., max_length=255, description="Quận/Huyện")
    ward: str = Field(..., max_length=255, description="Xã/Phường")
    address_detail: str = Field(..., max_length=500, description="Địa chỉ chi tiết")
    is_default: bool = Field(False, description="Đặt làm địa chỉ mặc định")

class ShippingAddressCreate(ShippingAddressBase):
    pass

class ShippingAddressUpdate(BaseModel):
    receiver_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    province: Optional[str] = Field(None, max_length=255)
    district: Optional[str] = Field(None, max_length=255)
    ward: Optional[str] = Field(None, max_length=255)
    address_detail: Optional[str] = Field(None, max_length=500)
    is_default: Optional[bool] = None

class ShippingAddressResponse(ShippingAddressBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
