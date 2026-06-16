import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import BIGINT, DECIMAL, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class PaymentProvider(str, enum.Enum):
    VNPAY = "VNPAY"
    MOMO = "MOMO"
    STRIPE = "STRIPE"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Payment(Base, TimestampMixin):
    """
    Bảng `payments` — Lịch sử thanh toán
    """
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("orders.id"))
    provider: Mapped[PaymentProvider] = mapped_column(Enum(PaymentProvider), nullable=False)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payments"
    )
