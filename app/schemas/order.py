from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    receiver_name: str = Field(..., max_length=255, description="Tên người nhận")
    phone: str = Field(..., max_length=20, description="Số điện thoại người nhận")
    province: str = Field(..., max_length=255, description="Tỉnh/Thành phố")
    district: str = Field(..., max_length=255, description="Quận/Huyện")
    ward: str = Field(..., max_length=255, description="Xã/Phường")
    address_detail: str = Field(..., max_length=500, description="Địa chỉ chi tiết")
    note: Optional[str] = Field(None, description="Ghi chú đơn hàng")
    coupon_id: Optional[int] = Field(None, description="ID mã giảm giá nếu có")
    payment_method: str = Field("COD", description="Phương thức thanh toán: COD | VNPAY | MOMO")

class OrderResponse(BaseModel):
    id: int
    order_code: str
    subtotal: float
    discount_amount: float
    shipping_fee: float
    total_price: float
    status: OrderStatus
    note: Optional[str] = None
    receiver_name: Optional[str] = None
    phone: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    address_detail: Optional[str] = None
    payment_method: str = "COD"
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
