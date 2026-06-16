from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.review import Review
from app.models.product import Product
from app.repositories.base import BaseRepository
from app.schemas.review import ReviewCreate, ReviewUpdate
from typing import List

class ReviewRepository(BaseRepository[Review, ReviewCreate, ReviewUpdate]):
    def get_by_product(self, db: Session, product_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
        return db.query(Review).filter(Review.product_id == product_id).offset(skip).limit(limit).all()

    def update_product_rating(self, db: Session, product_id: int):
        # Tính toán average rating và total reviews
        result = db.query(
            func.avg(Review.rating).label('average'),
            func.count(Review.id).label('total')
        ).filter(Review.product_id == product_id).first()
        
        avg_rating = float(result.average) if result.average else 0.0
        total_reviews = result.total if result.total else 0
        
        # Cập nhật vào Product
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.average_rating = avg_rating
            product.total_reviews = total_reviews
            db.commit()

review_repo = ReviewRepository(Review)
