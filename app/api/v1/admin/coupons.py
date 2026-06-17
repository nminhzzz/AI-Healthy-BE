from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.admin.users import require_admin
from app.models.user import User
from app.schemas.coupon import CouponCreate, CouponUpdate, CouponResponse
from app.repositories.coupon_repo import coupon_repo

router = APIRouter()

@router.get("/", response_model=List[CouponResponse])
def get_coupons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Lấy danh sách toàn bộ mã giảm giá (Admin).
    """
    return coupon_repo.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=CouponResponse, status_code=status.HTTP_201_CREATED)
def create_coupon(
    coupon_in: CouponCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Tạo mới một mã giảm giá (Admin).
    """
    existing_coupon = coupon_repo.get_by_code(db, code=coupon_in.code)
    if existing_coupon:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mã giảm giá '{coupon_in.code}' đã tồn tại trong hệ thống."
        )
    return coupon_repo.create(db, obj_in=coupon_in)


@router.put("/{coupon_id}", response_model=CouponResponse)
def update_coupon(
    coupon_id: int,
    coupon_in: CouponUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Cập nhật thông tin mã giảm giá (Admin).
    """
    db_coupon = coupon_repo.get(db, id=coupon_id)
    if not db_coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy mã giảm giá."
        )
        
    if coupon_in.code and coupon_in.code != db_coupon.code:
        existing_coupon = coupon_repo.get_by_code(db, code=coupon_in.code)
        if existing_coupon:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mã giảm giá '{coupon_in.code}' đã tồn tại."
            )
            
    return coupon_repo.update(db, db_obj=db_coupon, obj_in=coupon_in)


@router.delete("/{coupon_id}")
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Xóa mã giảm giá (Admin).
    """
    db_coupon = coupon_repo.get(db, id=coupon_id)
    if not db_coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy mã giảm giá."
        )
    coupon_repo.delete(db, id=coupon_id)
    return {"message": "Xóa mã giảm giá thành công."}
