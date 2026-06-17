from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from typing import List

from app.api.deps import get_db, get_redis, get_current_user
from app.models.user import User
from app.schemas.cart import CartResponse, CartItemSchema
from app.services.cart_service import cart_service
from app.repositories.cart_repo import cart_repo

router = APIRouter()

@router.get("/", response_model=CartResponse)
async def get_cart(
    db: Session = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """Lấy thông tin chi tiết các sản phẩm trong giỏ hàng hiện tại."""
    return await cart_service.get_cart_detail(db, redis_client, current_user.id)

@router.post("/items", status_code=status.HTTP_200_OK)
async def add_item_to_cart(
    item_in: CartItemSchema,
    redis_client: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """Thêm sản phẩm vào giỏ hàng hoặc tăng số lượng."""
    await cart_repo.add_to_cart(redis_client, current_user.id, item_in.product_id, item_in.quantity)
    return {"message": "Đã thêm sản phẩm vào giỏ hàng thành công."}

@router.put("/items", status_code=status.HTTP_200_OK)
async def update_cart_item(
    item_in: CartItemSchema,
    redis_client: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """Cập nhật chính xác số lượng sản phẩm trong giỏ hàng."""
    await cart_repo.update_cart_item(redis_client, current_user.id, item_in.product_id, item_in.quantity)
    return {"message": "Đã cập nhật số lượng sản phẩm thành công."}

@router.delete("/items/{product_id}", status_code=status.HTTP_200_OK)
async def remove_item_from_cart(
    product_id: int,
    redis_client: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """Xóa hẳn một sản phẩm khỏi giỏ hàng."""
    await cart_repo.remove_from_cart(redis_client, current_user.id, product_id)
    return {"message": "Đã xóa sản phẩm khỏi giỏ hàng."}

@router.delete("/", status_code=status.HTTP_200_OK)
async def clear_cart(
    redis_client: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """Xóa sạch giỏ hàng."""
    await cart_repo.clear_cart(redis_client, current_user.id)
    return {"message": "Đã làm trống giỏ hàng thành công."}

@router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_guest_cart(
    items_in: List[CartItemSchema],
    redis_client: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """Đồng bộ hóa giỏ hàng khách từ LocalStorage lên Redis sau khi đăng nhập."""
    items = [item.model_dump() for item in items_in]
    await cart_repo.sync_cart(redis_client, current_user.id, items)
    return {"message": "Đồng bộ hóa giỏ hàng thành công."}
