from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.wishlist import Wishlist
from app.models.product import Product
from typing import List

class WishlistService:
    def get_user_wishlist(self, db: Session, user_id: int) -> List[Wishlist]:
        """Lấy toàn bộ sản phẩm yêu thích của người dùng."""
        return db.query(Wishlist).filter(Wishlist.user_id == user_id).order_by(Wishlist.created_at.desc()).all()

    def toggle_wishlist(self, db: Session, user_id: int, product_id: int) -> bool:
        """Thêm hoặc xóa sản phẩm khỏi danh sách yêu thích. Trả về True nếu thêm mới, False nếu xóa đi."""
        # Kiểm tra sản phẩm có tồn tại không
        product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sản phẩm không tồn tại hoặc đã ngừng kinh doanh."
            )

        # Kiểm tra xem sản phẩm đã có trong wishlist chưa
        item = db.query(Wishlist).filter(
            Wishlist.user_id == user_id,
            Wishlist.product_id == product_id
        ).first()

        if item:
            # Nếu đã có, tiến hành xóa
            db.delete(item)
            db.commit()
            return False
        else:
            # Nếu chưa có, tiến hành thêm mới
            new_item = Wishlist(user_id=user_id, product_id=product_id)
            db.add(new_item)
            db.commit()
            return True

wishlist_service = WishlistService()
