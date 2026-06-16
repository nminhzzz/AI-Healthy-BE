from typing import Optional

from sqlalchemy import BIGINT, Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Review(Base, TimestampMixin):
    """
    Bảng `reviews` — Đánh giá sản phẩm
    """
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("products.id"))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verified_purchase: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews"
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="reviews"
    )
