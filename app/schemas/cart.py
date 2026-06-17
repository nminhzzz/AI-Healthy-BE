from pydantic import BaseModel, Field
from typing import List
from app.schemas.product import ProductResponse

class CartItemSchema(BaseModel):
    product_id: int = Field(..., description="ID sản phẩm")
    quantity: int = Field(..., ge=1, description="Số lượng sản phẩm, tối thiểu là 1")

class CartItemDetailResponse(BaseModel):
    product_id: int
    quantity: int
    product: ProductResponse

class CartResponse(BaseModel):
    items: List[CartItemDetailResponse] = []
    total_price: float = Field(0.0, description="Tổng tiền giỏ hàng")
