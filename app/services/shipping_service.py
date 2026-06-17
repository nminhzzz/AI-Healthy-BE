from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.shipping import ShippingAddress
from app.schemas.shipping import ShippingAddressCreate, ShippingAddressUpdate
from typing import List

class ShippingService:
    def get_user_addresses(self, db: Session, user_id: int) -> List[ShippingAddress]:
        """Lấy danh sách địa chỉ đã lưu của người dùng (địa chỉ mặc định lên đầu)."""
        return (
            db.query(ShippingAddress)
            .filter(ShippingAddress.user_id == user_id)
            .order_by(ShippingAddress.is_default.desc(), ShippingAddress.created_at.desc())
            .all()
        )

    def create_address(self, db: Session, user_id: int, address_in: ShippingAddressCreate) -> ShippingAddress:
        """Tạo địa chỉ giao nhận mới."""
        # Kiểm tra xem đây có phải địa chỉ đầu tiên không
        existing_count = db.query(ShippingAddress).filter(ShippingAddress.user_id == user_id).count()
        is_default = address_in.is_default
        if existing_count == 0:
            is_default = True

        # Nếu đặt địa chỉ này làm mặc định, đặt các địa chỉ khác thành không mặc định
        if is_default:
            db.query(ShippingAddress).filter(ShippingAddress.user_id == user_id).update({"is_default": False})

        db_address = ShippingAddress(
            user_id=user_id,
            receiver_name=address_in.receiver_name,
            phone=address_in.phone,
            province=address_in.province,
            district=address_in.district,
            ward=address_in.ward,
            address_detail=address_in.address_detail,
            is_default=is_default
        )
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address

    def update_address(self, db: Session, user_id: int, address_id: int, address_in: ShippingAddressUpdate) -> ShippingAddress:
        """Cập nhật thông tin địa chỉ giao nhận."""
        db_address = db.query(ShippingAddress).filter(
            ShippingAddress.id == address_id,
            ShippingAddress.user_id == user_id
        ).first()

        if not db_address:
            raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ giao nhận.")

        update_data = address_in.model_dump(exclude_unset=True)

        if "is_default" in update_data and update_data["is_default"]:
            # Đặt tất cả địa chỉ khác thành không mặc định
            db.query(ShippingAddress).filter(ShippingAddress.user_id == user_id).update({"is_default": False})

        for key, value in update_data.items():
            setattr(db_address, key, value)

        db.commit()
        db.refresh(db_address)
        return db_address

    def delete_address(self, db: Session, user_id: int, address_id: int) -> None:
        """Xóa địa chỉ giao nhận và tự động thiết lập lại mặc định nếu cần."""
        db_address = db.query(ShippingAddress).filter(
            ShippingAddress.id == address_id,
            ShippingAddress.user_id == user_id
        ).first()

        if not db_address:
            raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ giao nhận.")

        was_default = db_address.is_default
        db.delete(db_address)
        db.commit()

        # Nếu địa chỉ bị xóa là địa chỉ mặc định, chọn địa chỉ gần nhất làm mặc định mới
        if was_default:
            next_address = db.query(ShippingAddress).filter(
                ShippingAddress.user_id == user_id
            ).order_by(ShippingAddress.created_at.desc()).first()
            if next_address:
                next_address.is_default = True
                db.commit()

    def set_default_address(self, db: Session, user_id: int, address_id: int) -> ShippingAddress:
        """Đặt một địa chỉ cụ thể làm mặc định."""
        db_address = db.query(ShippingAddress).filter(
            ShippingAddress.id == address_id,
            ShippingAddress.user_id == user_id
        ).first()

        if not db_address:
            raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ giao nhận.")

        # Đặt toàn bộ thành không mặc định
        db.query(ShippingAddress).filter(ShippingAddress.user_id == user_id).update({"is_default": False})
        
        # Đặt địa chỉ này thành mặc định
        db_address.is_default = True
        db.commit()
        db.refresh(db_address)
        return db_address

shipping_service = ShippingService()
