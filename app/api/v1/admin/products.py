from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import product_service
from app.repositories.product_repo import product_repo

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0, limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return product_repo.search(db, skip=skip, limit=limit, category_id=category_id, search_query=search)

@router.post("/", response_model=ProductResponse)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return product_service.create_product(db, product_in)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return product_service.update_product(db, product_id, product_in)

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = product_repo.delete(db, id=product_id)
    return {"message": "Product deleted successfully" if product else "Product not found"}
