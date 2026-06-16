from datetime import datetime

from sqlalchemy import BIGINT, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Wishlist(Base):
    """
    Bảng `wishlists` — Danh sách yêu thích
    """
    __tablename__ = "wishlists"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("products.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="wishlists"
    )
    product: Mapped["Product"] = relationship("Product")
