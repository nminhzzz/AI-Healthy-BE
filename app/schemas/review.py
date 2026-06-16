from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Điểm đánh giá từ 1 đến 5")
    comment: Optional[str] = Field(None, description="Bình luận")


class ReviewCreate(ReviewBase):
    product_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
