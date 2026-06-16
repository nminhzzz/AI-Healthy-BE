from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.mongodb import close_mongodb_connection, connect_to_mongodb
from app.db.mysql import engine
from app.db.redis import close_redis_connection, connect_to_redis
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events: Quản lý vòng đời ứng dụng FastAPI.
    Thay thế cho @app.on_event("startup") và @app.on_event("shutdown").
    """
    # --- Startup ---
    # 1. Kết nối MongoDB
    await connect_to_mongodb()
    
    # 2. Kết nối Redis
    await connect_to_redis()
    
    # 3. Tạo bảng MySQL (Nên dùng Alembic trong môi trường Production)
    # Hàm này sẽ tạo các bảng dựa trên class kế thừa từ `Base` nếu chưa tồn tại
    Base.metadata.create_all(bind=engine)
    
    yield  # Ứng dụng chạy
    
    # --- Shutdown ---
    await close_mongodb_connection()
    await close_redis_connection()


# Khởi tạo FastAPI
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API cho HealthShop AI",
    lifespan=lifespan,
    debug=settings.debug,
)


# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.api.v1.api import api_router

@app.get("/")
async def root():
    return {
        "message": "Welcome to HealthShop AI API",
        "env": settings.app_env,
        "docs_url": "/docs"
    }

app.include_router(api_router, prefix="/api/v1")
