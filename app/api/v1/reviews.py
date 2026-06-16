from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.review_service import review_service
from app.repositories.review_repo import review_repo

router = APIRouter()

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(
    product_id: int,
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    return review_repo.get_by_product(db, product_id=product_id, skip=skip, limit=limit)

@router.post("/", response_model=ReviewResponse)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return review_service.create_review(db, current_user.id, review_in)
