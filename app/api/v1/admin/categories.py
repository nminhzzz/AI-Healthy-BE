from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import category_service
from app.repositories.category_repo import category_repo

router = APIRouter()

# TODO: Add Depends to check if user is admin
@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return category_repo.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=CategoryResponse)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return category_service.create_category(db, category_in)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return category_service.update_category(db, category_id, category_in)

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = category_repo.delete(db, id=category_id)
    return {"message": "Category deleted successfully" if category else "Category not found"}
