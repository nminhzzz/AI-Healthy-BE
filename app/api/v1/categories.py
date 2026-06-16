from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.category import CategoryResponse
from app.services.category_service import category_service
from app.repositories.category_repo import category_repo

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    return category_repo.get_all(db, skip=skip, limit=limit)

@router.get("/{slug}", response_model=CategoryResponse)
def get_category_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    return category_service.get_category_by_slug(db, slug)
