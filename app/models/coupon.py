from datetime import datetime
from typing import Optional

from sqlalchemy import BIGINT, Boolean, DECIMAL, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Coupon(Base, TimestampMixin):
    """
    Bảng `coupons` — Mã giảm giá
    """
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    discount_amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="coupon"
    )
