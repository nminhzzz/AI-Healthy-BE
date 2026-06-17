from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from typing import List

from app.api.deps import get_db, get_redis, get_current_user
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import order_service
from app.repositories.order_repo import order_repo

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """Đặt hàng từ giỏ hàng hiện tại."""
    return await order_service.create_order(db, redis_client, current_user.id, order_in)

@router.get("/", response_model=List[OrderResponse])
def get_order_history(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy lịch sử đơn hàng của người dùng hiện tại."""
    return order_repo.get_user_orders(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy chi tiết một đơn hàng cụ thể."""
    return order_service.get_order_detail(db, user_id=current_user.id, order_id=order_id)

@router.put("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Hủy đơn hàng đang chờ duyệt."""
    return order_service.cancel_order(db, user_id=current_user.id, order_id=order_id)
