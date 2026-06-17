from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api.deps import get_db
from app.api.v1.admin.users import require_admin
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderResponse
from app.services.order_service import order_service
from app.repositories.order_repo import order_repo

router = APIRouter()

@router.get("/", response_model=List[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[OrderStatus] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Lấy danh sách đơn hàng cho Admin.
    Hỗ trợ phân trang, lọc theo trạng thái và tìm kiếm (theo mã đơn hàng, tên người nhận, số điện thoại).
    """
    query = db.query(Order)
    
    # Lọc theo trạng thái
    if status:
        query = query.filter(Order.status == status)
        
    # Tìm kiếm
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Order.order_code.like(search_filter),
                Order.receiver_name.like(search_filter),
                Order.phone.like(search_filter)
            )
        )
        
    # Sắp xếp mới nhất lên đầu
    query = query.order_by(Order.created_at.desc())
    
    return query.offset(skip).limit(limit).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Lấy thông tin chi tiết một đơn hàng cụ thể cho Admin.
    """
    order = order_repo.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đơn hàng."
        )
    return order


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Cập nhật trạng thái đơn hàng (Admin).
    """
    return order_service.admin_update_order_status(db, order_id=order_id, new_status=new_status)
