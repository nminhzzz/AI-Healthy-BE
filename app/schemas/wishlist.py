from pydantic import BaseModel
from datetime import datetime
from app.schemas.product import ProductResponse

class WishlistResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    product: ProductResponse

    class Config:
        from_attributes = True

class WishlistToggleResponse(BaseModel):
    product_id: int
    in_wishlist: bool
    message: str
