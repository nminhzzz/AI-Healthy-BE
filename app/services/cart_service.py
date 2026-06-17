from sqlalchemy.orm import Session
from redis.asyncio import Redis
from app.repositories.cart_repo import cart_repo
from app.repositories.product_repo import product_repo
from app.schemas.cart import CartResponse, CartItemDetailResponse

class CartService:
    async def get_cart_detail(self, db: Session, redis_client: Redis, user_id: int) -> CartResponse:
        """Lấy giỏ hàng chi tiết kết hợp dữ liệu số lượng từ Redis và thông tin sản phẩm từ MySQL."""
        raw_items = await cart_repo.get_cart_items(redis_client, user_id)
        
        items_detail = []
        total_price = 0.0
        
        for p_id_str, qty_str in raw_items.items():
            try:
                product_id = int(p_id_str)
                quantity = int(qty_str)
            except ValueError:
                continue
                
            product = product_repo.get(db, id=product_id)
            # Chỉ hiển thị các sản phẩm còn kích hoạt hoạt động
            if product and product.is_active:
                price = product.sale_price if product.sale_price is not None else product.price
                total_price += float(price) * quantity
                
                items_detail.append(
                    CartItemDetailResponse(
                        product_id=product_id,
                        quantity=quantity,
                        product=product # Tự động deserialize qua ProductResponse
                    )
                )
                
        return CartResponse(items=items_detail, total_price=total_price)

cart_service = CartService()
