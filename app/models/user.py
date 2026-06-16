"""
User Models — HealthShop AI
Gồm 2 bảng MySQL theo thiết kế database (Giai đoạn 2):
  - users           : Tài khoản người dùng
  - health_profiles : Hồ sơ sức khỏe cá nhân (1-1 với users)
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BIGINT,
    FLOAT,
    TEXT,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class UserRole(str, enum.Enum):
    """Vai trò người dùng trong hệ thống."""
    USER  = "USER"
    ADMIN = "ADMIN"


class Gender(str, enum.Enum):
    """Giới tính trong hồ sơ sức khỏe."""
    MALE   = "MALE"
    FEMALE = "FEMALE"
    OTHER  = "OTHER"


# ---------------------------------------------------------------------------
# Model: User
# ---------------------------------------------------------------------------

class User(Base, TimestampMixin):
    """
    Bảng `users` — lưu tài khoản người dùng.

    Relationships:
        health_profile  → HealthProfile (one-to-one)
        reviews         → Review        (one-to-many)
        wishlists       → Wishlist      (one-to-many)
        orders          → Order         (one-to-many)
        shipping_addresses → ShippingAddress (one-to-many)
    """

    __tablename__ = "users"

    # ── Primary key ──────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
        comment="ID người dùng",
    )

    # ── Thông tin tài khoản ──────────────────────────────────────────────────
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Email đăng nhập (duy nhất)",
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Mật khẩu đã mã hóa bằng bcrypt",
    )

    # ── Thông tin cá nhân ────────────────────────────────────────────────────
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Họ và tên đầy đủ",
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="Số điện thoại",
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="URL ảnh đại diện",
    )

    # ── Phân quyền & trạng thái ──────────────────────────────────────────────
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
        comment="Vai trò: USER | ADMIN",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Trạng thái tài khoản (True = hoạt động)",
    )

    # ── Thời gian ────────────────────────────────────────────────────────────
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="Thời điểm đăng nhập lần cuối",
    )
    # created_at & updated_at kế thừa từ TimestampMixin

    # ── Relationships ─────────────────────────────────────────────────────────
    health_profile: Mapped[Optional["HealthProfile"]] = relationship(
        "HealthProfile",
        back_populates="user",
        uselist=False,          # one-to-one
        cascade="all, delete-orphan",
        lazy="select",
    )
    reviews: Mapped[list["Review"]] = relationship(          # type: ignore[name-defined]
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    wishlists: Mapped[list["Wishlist"]] = relationship(      # type: ignore[name-defined]
        "Wishlist",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    orders: Mapped[list["Order"]] = relationship(            # type: ignore[name-defined]
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    shipping_addresses: Mapped[list["ShippingAddress"]] = relationship(   # type: ignore[name-defined]
        "ShippingAddress",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )

    # ── Dunder ────────────────────────────────────────────────────────────────
    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role}>"


# ---------------------------------------------------------------------------
# Model: HealthProfile
# ---------------------------------------------------------------------------

class HealthProfile(Base, TimestampMixin):
    """
    Bảng `health_profiles` — hồ sơ sức khỏe cá nhân của từng user (1-1).

    Dùng bởi AI Product Advisor để tư vấn sản phẩm phù hợp:
      - Mục tiêu sức khỏe (goal): giảm cân, tăng cơ, bổ sung vitamin, ...
      - Dị ứng (allergies): danh sách dị ứng cách nhau bằng dấu phẩy
      - Bệnh nền (medical_conditions): danh sách bệnh lý liên quan
    """

    __tablename__ = "health_profiles"

    # ── Primary key ──────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
        comment="ID hồ sơ sức khỏe",
    )

    # ── Foreign key ──────────────────────────────────────────────────────────
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,            # 1 user chỉ có 1 health profile
        nullable=False,
        index=True,
        comment="FK → users.id",
    )

    # ── Thông tin sinh học ───────────────────────────────────────────────────
    gender: Mapped[Optional[Gender]] = mapped_column(
        Enum(Gender),
        nullable=True,
        comment="Giới tính: MALE | FEMALE | OTHER",
    )
    age: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Tuổi (năm)",
    )
    height: Mapped[Optional[float]] = mapped_column(
        FLOAT,
        nullable=True,
        comment="Chiều cao (cm)",
    )
    weight: Mapped[Optional[float]] = mapped_column(
        FLOAT,
        nullable=True,
        comment="Cân nặng (kg)",
    )

    # ── Thông tin sức khỏe ───────────────────────────────────────────────────
    goal: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment=(
            "Mục tiêu sức khỏe. VD: 'Giảm cân', 'Tăng cơ', "
            "'Bổ sung vitamin', 'Ngủ ngon hơn'"
        ),
    )
    allergies: Mapped[Optional[str]] = mapped_column(
        TEXT,
        nullable=True,
        comment="Danh sách dị ứng, cách nhau bằng dấu phẩy. VD: 'Gluten, Sữa bò'",
    )
    medical_conditions: Mapped[Optional[str]] = mapped_column(
        TEXT,
        nullable=True,
        comment=(
            "Bệnh nền / tình trạng y tế. "
            "VD: 'Tiểu đường type 2, Huyết áp cao'"
        ),
    )
    # created_at & updated_at kế thừa từ TimestampMixin

    # ── Relationships ─────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship(
        "User",
        back_populates="health_profile",
    )

    # ── Dunder ────────────────────────────────────────────────────────────────
    def __repr__(self) -> str:
        return (
            f"<HealthProfile id={self.id} user_id={self.user_id} "
            f"goal={self.goal!r}>"
        )
