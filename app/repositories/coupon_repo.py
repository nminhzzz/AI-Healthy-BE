from sqlalchemy.orm import Session
from app.models.coupon import Coupon
from app.repositories.base import BaseRepository
from app.schemas.coupon import CouponCreate, CouponUpdate

class CouponRepository(BaseRepository[Coupon, CouponCreate, CouponUpdate]):
    def get_by_code(self, db: Session, code: str) -> Coupon | None:
        return db.query(Coupon).filter(Coupon.code == code).first()

coupon_repo = CouponRepository(Coupon)
