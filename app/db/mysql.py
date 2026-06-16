from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Khởi tạo engine kết nối MySQL (đồng bộ)
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Tự động ping để kiểm tra kết nối trước khi sử dụng
    pool_recycle=3600,   # Tái tạo kết nối sau 1 giờ
    echo=False,          # Tắt in log SQL thô ra console để tránh rối mắt
)

# Tạo class SessionLocal để cấp phát session cho mỗi request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency generator dùng trong FastAPI endpoints để lấy DB session.
    Cách dùng: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
