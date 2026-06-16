from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.product import ProductResponse, ProductResponseWithCategory
from app.services.product_service import product_service
from app.repositories.product_repo import product_repo

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0, limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Public only sees active products
    return product_repo.search(db, skip=skip, limit=limit, category_id=category_id, search_query=search, is_active=True)

@router.get("/{slug}", response_model=ProductResponseWithCategory)
def get_product_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    return product_service.get_product_by_slug(db, slug)
