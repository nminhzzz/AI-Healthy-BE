from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    category_id: int
    sku: str = Field(..., max_length=100)
    brand: Optional[str] = Field(None, max_length=255)
    price: float = Field(..., ge=0)
    sale_price: Optional[float] = Field(None, ge=0)
    stock: int = Field(0, ge=0)
    
    description: Optional[str] = None
    ingredients: Optional[str] = None
    usage_guide: Optional[str] = None
    benefits: Optional[str] = None
    warnings: Optional[str] = None
    
    image_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = Field(True)


class ProductCreate(ProductBase):
    slug: Optional[str] = Field(None, max_length=255)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None
    slug: Optional[str] = Field(None, max_length=255)
    sku: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = Field(None, ge=0)
    sale_price: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    
    description: Optional[str] = None
    ingredients: Optional[str] = None
    usage_guide: Optional[str] = None
    benefits: Optional[str] = None
    warnings: Optional[str] = None
    
    image_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    slug: str
    average_rating: Optional[float] = 0.0
    total_reviews: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductResponseWithCategory(ProductResponse):
    category: Optional[CategoryResponse] = None
