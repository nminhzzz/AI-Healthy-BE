from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import Dict
from app.api.deps import get_current_user
from app.models.user import User
from app.services.cloudinary_service import upload_image

router = APIRouter()

@router.post("/image", response_model=Dict[str, str])
async def upload_image_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload một hình ảnh lên Cloudinary.
    Chỉ dành cho user đã đăng nhập (bao gồm Admin).
    """
    # 1. Kiểm tra định dạng file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # 2. Đọc file
    file_bytes = await file.read()

    # 3. Giới hạn kích thước (vd: 5MB)
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds 5MB")

    try:
        # 4. Upload lên Cloudinary
        image_url = upload_image(file_bytes, folder="healthshop/uploads")
        return {"url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
