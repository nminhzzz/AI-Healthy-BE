import logging
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_mongo = MongoDB()

async def connect_to_mongodb():
    """Khởi tạo kết nối MongoDB (gọi khi FastAPI app startup)."""
    logger.info("Đang kết nối tới MongoDB...")
    db_mongo.client = AsyncIOMotorClient(settings.mongodb_url)
    db_mongo.db = db_mongo.client[settings.mongodb_db]
    logger.info(f"Đã kết nối MongoDB: {settings.mongodb_db}")

async def close_mongodb_connection():
    """Đóng kết nối MongoDB (gọi khi FastAPI app shutdown)."""
    if db_mongo.client:
        db_mongo.client.close()
        logger.info("Đã đóng kết nối MongoDB.")

def get_mongodb():
    """Dependency lấy MongoDB database object."""
    return db_mongo.db
