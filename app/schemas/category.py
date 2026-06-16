from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255, description="Tên danh mục")
    description: Optional[str] = Field(None, description="Mô tả danh mục")
    image_url: Optional[str] = Field(None, max_length=500, description="URL hình ảnh")
    is_active: bool = Field(True, description="Trạng thái hoạt động")


class CategoryCreate(CategoryBase):
    slug: Optional[str] = Field(None, max_length=255, description="Slug (tùy chọn, nếu để trống sẽ tự tạo từ name)")


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
