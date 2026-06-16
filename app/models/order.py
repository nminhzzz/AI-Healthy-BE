import enum
from typing import Optional

from sqlalchemy import BIGINT, DECIMAL, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPING = "SHIPPING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(Base, TimestampMixin):
    """
    Bảng `orders` — Đơn hàng
    """
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"))
    coupon_id: Mapped[Optional[int]] = mapped_column(BIGINT, ForeignKey("coupons.id"), nullable=True)
    order_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    subtotal: Mapped[float] = mapped_column(DECIMAL(12, 2), default=0.0)
    discount_amount: Mapped[float] = mapped_column(DECIMAL(12, 2), default=0.0)
    shipping_fee: Mapped[float] = mapped_column(DECIMAL(12, 2), default=0.0)
    total_price: Mapped[float] = mapped_column(DECIMAL(12, 2), default=0.0)
    
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="orders"
    )
    coupon: Mapped[Optional["Coupon"]] = relationship(
        "Coupon",
        back_populates="orders"
    )
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    """
    Bảng `order_items` — Chi tiết sản phẩm trong đơn hàng
    """
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("products.id"))
    
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items"
    )
