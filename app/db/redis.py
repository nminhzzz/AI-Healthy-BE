import logging
import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisDB:
    client: redis.Redis = None

db_redis = RedisDB()

async def connect_to_redis():
    """Khởi tạo kết nối Redis (gọi khi FastAPI app startup)."""
    logger.info("Đang kết nối tới Redis...")
    db_redis.client = redis.from_url(
        settings.redis_url, 
        encoding="utf-8", 
        decode_responses=True
    )
    # Ping thử để đảm bảo kết nối thành công
    await db_redis.client.ping()
    logger.info("Đã kết nối Redis.")

async def close_redis_connection():
    """Đóng kết nối Redis (gọi khi FastAPI app shutdown)."""
    if db_redis.client:
        await db_redis.client.close()
        logger.info("Đã đóng kết nối Redis.")

def get_redis() -> redis.Redis:
    """Dependency lấy Redis client object."""
    return db_redis.client
