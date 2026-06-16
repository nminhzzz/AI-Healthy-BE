from typing import Optional

from sqlalchemy import BIGINT, Boolean, DECIMAL, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Product(Base, TimestampMixin):
    """
    Bảng `products` — Sản phẩm
    """
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    brand: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    sale_price: Mapped[Optional[float]] = mapped_column(DECIMAL(12, 2), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    
    # Text contents
    description: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)
    ingredients: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)
    usage_guide: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)
    benefits: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)
    warnings: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)
    
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    average_rating: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan",
    )
