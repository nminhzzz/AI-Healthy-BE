from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.payment import PaymentProvider, PaymentStatus

class PaymentCreate(BaseModel):
    order_id: int
    provider: PaymentProvider = Field(PaymentProvider.VNPAY, description="Nhà cung cấp thanh toán")

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    provider: PaymentProvider
    transaction_id: Optional[str] = None
    amount: float
    status: PaymentStatus
    paid_at: Optional[datetime] = None
    created_at: datetime
    payment_url: Optional[str] = None

    class Config:
        from_attributes = True
