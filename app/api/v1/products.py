from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.product import ProductResponse, ProductResponseWithCategory, ProductSearchResponse
from app.services.product_service import product_service
from app.repositories.product_repo import product_repo

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0, limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Public only sees active products
    return product_repo.search(
        db, 
        skip=skip, 
        limit=limit, 
        category_id=category_id, 
        search_query=search, 
        is_active=True,
        price_min=price_min,
        price_max=price_max,
        sort_by=sort_by
    )

@router.get("/search", response_model=ProductSearchResponse)
def search_products(
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    brand: Optional[str] = None,
    sort_by: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 20
    skip = (page - 1) * limit
    
    items, total = product_repo.search_advanced(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        search_query=q,
        is_active=True,
        price_min=price_min,
        price_max=price_max,
        brand=brand,
        sort_by=sort_by
    )
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }

@router.get("/{slug}", response_model=ProductResponseWithCategory)
def get_product_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    return product_service.get_product_by_slug(db, slug)
