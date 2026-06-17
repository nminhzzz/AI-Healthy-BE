from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.wishlist import WishlistResponse, WishlistToggleResponse
from app.services.wishlist_service import wishlist_service

router = APIRouter()

@router.get("/", response_model=List[WishlistResponse])
def get_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy danh sách sản phẩm yêu thích của người dùng hiện tại.
    """
    return wishlist_service.get_user_wishlist(db, user_id=current_user.id)


@router.post("/toggle/{product_id}", response_model=WishlistToggleResponse)
def toggle_wishlist_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Thêm/Xóa sản phẩm khỏi danh sách yêu thích của người dùng hiện tại.
    """
    in_wishlist = wishlist_service.toggle_wishlist(db, user_id=current_user.id, product_id=product_id)
    message = "Đã thêm sản phẩm vào danh sách yêu thích." if in_wishlist else "Đã xóa sản phẩm khỏi danh sách yêu thích."
    return {
        "product_id": product_id,
        "in_wishlist": in_wishlist,
        "message": message
    }
