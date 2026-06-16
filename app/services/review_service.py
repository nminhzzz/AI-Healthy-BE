from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.review_repo import review_repo
from app.repositories.product_repo import product_repo
from app.schemas.review import ReviewCreate

class ReviewService:
    def create_review(self, db: Session, user_id: int, review_in: ReviewCreate):
        # Kiểm tra product có tồn tại không
        product = product_repo.get(db, id=review_in.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Optional: Kiểm tra user có mua hàng chưa (Business Logic nâng cao)
        # Tạm thời bỏ qua phần kiểm tra này như plan.

        review_data = review_in.model_dump()
        review_data["user_id"] = user_id
        
        # Thêm vào DB (cần class trung gian hoặc dùng create_schema nhưng có user_id)
        from app.models.review import Review
        new_review = Review(**review_data)
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        # Cập nhật average rating
        review_repo.update_product_rating(db, product_id=review_in.product_id)

        return new_review

review_service = ReviewService()
