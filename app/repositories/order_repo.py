from sqlalchemy.orm import Session
from app.models.order import Order
from app.repositories.base import BaseRepository
from typing import List, Optional, Any

class OrderRepository(BaseRepository[Order, Any, Any]):
    def get_user_orders(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Lấy lịch sử đơn hàng của người dùng, sắp xếp mới nhất lên đầu."""
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_code(self, db: Session, order_code: str) -> Optional[Order]:
        """Lấy chi tiết đơn hàng thông qua mã đơn hàng."""
        return db.query(Order).filter(Order.order_code == order_code).first()

order_repo = OrderRepository(Order)
