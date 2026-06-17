from redis.asyncio import Redis
from typing import Dict, List

class CartRepository:
    def _get_key(self, user_id: int) -> str:
        return f"cart:user:{user_id}"

    async def get_cart_items(self, redis_client: Redis, user_id: int) -> Dict[str, str]:
        """Lấy danh sách các cặp {product_id: quantity} trong giỏ hàng."""
        key = self._get_key(user_id)
        return await redis_client.hgetall(key)

    async def add_to_cart(self, redis_client: Redis, user_id: int, product_id: int, quantity: int):
        """Thêm sản phẩm vào giỏ hàng hoặc cộng dồn số lượng."""
        key = self._get_key(user_id)
        await redis_client.hincrby(key, str(product_id), quantity)

    async def update_cart_item(self, redis_client: Redis, user_id: int, product_id: int, quantity: int):
        """Cập nhật chính xác số lượng sản phẩm. Nếu số lượng <= 0, xóa khỏi giỏ."""
        key = self._get_key(user_id)
        if quantity <= 0:
            await redis_client.hdel(key, str(product_id))
        else:
            await redis_client.hset(key, str(product_id), quantity)

    async def remove_from_cart(self, redis_client: Redis, user_id: int, product_id: int):
        """Xóa hẳn một sản phẩm khỏi giỏ hàng."""
        key = self._get_key(user_id)
        await redis_client.hdel(key, str(product_id))

    async def clear_cart(self, redis_client: Redis, user_id: int):
        """Xóa sạch giỏ hàng của người dùng."""
        key = self._get_key(user_id)
        await redis_client.delete(key)

    async def sync_cart(self, redis_client: Redis, user_id: int, items: List[dict]):
        """Gộp giỏ hàng tạm thời từ LocalStorage của Frontend vào Redis sau khi đăng nhập."""
        key = self._get_key(user_id)
        for item in items:
            p_id = str(item.get("product_id"))
            qty = item.get("quantity", 0)
            if p_id and qty > 0:
                await redis_client.hincrby(key, p_id, qty)

cart_repo = CartRepository()
