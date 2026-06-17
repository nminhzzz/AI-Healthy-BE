from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.shipping import ShippingAddressCreate, ShippingAddressUpdate, ShippingAddressResponse
from app.services.shipping_service import shipping_service

router = APIRouter()

@router.get("/", response_model=List[ShippingAddressResponse])
def get_shipping_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy toàn bộ danh sách địa chỉ nhận hàng của người dùng.
    """
    return shipping_service.get_user_addresses(db, user_id=current_user.id)


@router.post("/", response_model=ShippingAddressResponse, status_code=status.HTTP_201_CREATED)
def create_shipping_address(
    address_in: ShippingAddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Tạo địa chỉ nhận hàng mới.
    """
    return shipping_service.create_address(db, user_id=current_user.id, address_in=address_in)


@router.put("/{address_id}", response_model=ShippingAddressResponse)
def update_shipping_address(
    address_id: int,
    address_in: ShippingAddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cập nhật thông tin địa chỉ nhận hàng.
    """
    return shipping_service.update_address(db, user_id=current_user.id, address_id=address_id, address_in=address_in)


@router.delete("/{address_id}")
def delete_shipping_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Xóa địa chỉ nhận hàng.
    """
    shipping_service.delete_address(db, user_id=current_user.id, address_id=address_id)
    return {"message": "Xóa địa chỉ nhận hàng thành công."}


@router.put("/{address_id}/default", response_model=ShippingAddressResponse)
def set_default_shipping_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Đặt địa chỉ nhận hàng làm mặc định.
    """
    return shipping_service.set_default_address(db, user_id=current_user.id, address_id=address_id)
