import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.core.config import settings

def init_cloudinary():
    """Khởi tạo kết nối Cloudinary"""
    if settings.cloudinary_cloud_name and settings.cloudinary_api_key and settings.cloudinary_api_secret:
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True
        )

def upload_image(file_bytes: bytes, folder: str = "healthshop") -> str:
    """
    Tải file ảnh lên Cloudinary
    :param file_bytes: Dữ liệu nhị phân của ảnh
    :param folder: Thư mục lưu trên Cloudinary
    :return: URL ảnh tĩnh (secure_url)
    """
    try:
        init_cloudinary()
        # Dùng file_bytes để upload trực tiếp không cần lưu tạm
        response = cloudinary.uploader.upload(
            file_bytes,
            folder=folder,
            resource_type="image"
        )
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload error: {str(e)}")
        raise e
