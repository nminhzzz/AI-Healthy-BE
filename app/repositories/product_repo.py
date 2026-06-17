from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.base import BaseRepository
from app.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional

class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    def get_by_slug(self, db: Session, slug: str) -> Product | None:
        return db.query(Product).filter(Product.slug == slug).first()

    def get_by_sku(self, db: Session, sku: str) -> Product | None:
        return db.query(Product).filter(Product.sku == sku).first()

    def search(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        category_id: Optional[int] = None,
        search_query: Optional[str] = None,
        is_active: Optional[bool] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        sort_by: Optional[str] = None
    ) -> List[Product]:
        from sqlalchemy import or_
        query = db.query(Product)
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        if price_min is not None:
            query = query.filter(Product.price >= price_min)
        if price_max is not None:
            query = query.filter(Product.price <= price_max)
            
        if search_query:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search_query}%"),
                    Product.brand.ilike(f"%{search_query}%"),
                    Product.sku.ilike(f"%{search_query}%"),
                    Product.description.ilike(f"%{search_query}%")
                )
            )
            
        # Áp dụng sắp xếp
        if sort_by == "price_asc":
            query = query.order_by(Product.price.asc())
        elif sort_by == "price_desc":
            query = query.order_by(Product.price.desc())
        elif sort_by == "name_asc":
            query = query.order_by(Product.name.asc())
        elif sort_by == "name_desc":
            query = query.order_by(Product.name.desc())
        elif sort_by == "rating_desc":
            query = query.order_by(Product.average_rating.desc())
        elif sort_by == "newest":
            query = query.order_by(Product.created_at.desc())
        else:
            query = query.order_by(Product.id.desc())
            
        return query.offset(skip).limit(limit).all()

    def search_advanced(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        search_query: Optional[str] = None,
        is_active: Optional[bool] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        brand: Optional[str] = None,
        sort_by: Optional[str] = None
    ) -> tuple[List[Product], int]:
        from sqlalchemy import or_
        query = db.query(Product)
        
        # Áp dụng bộ lọc trạng thái kích hoạt
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
            
        # Áp dụng bộ lọc danh mục
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
            
        # Áp dụng bộ lọc khoảng giá
        if price_min is not None:
            query = query.filter(Product.price >= price_min)
        if price_max is not None:
            query = query.filter(Product.price <= price_max)
            
        # Áp dụng bộ lọc thương hiệu
        if brand:
            query = query.filter(Product.brand == brand)
            
        # Áp dụng tìm kiếm đa trường
        if search_query:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search_query}%"),
                    Product.brand.ilike(f"%{search_query}%"),
                    Product.sku.ilike(f"%{search_query}%"),
                    Product.description.ilike(f"%{search_query}%")
                )
            )
            
        # Lấy tổng số lượng bản ghi khớp (trước khi phân trang)
        total = query.count()
        
        # Áp dụng sắp xếp
        if sort_by == "price_asc":
            query = query.order_by(Product.price.asc())
        elif sort_by == "price_desc":
            query = query.order_by(Product.price.desc())
        elif sort_by == "name_asc":
            query = query.order_by(Product.name.asc())
        elif sort_by == "name_desc":
            query = query.order_by(Product.name.desc())
        elif sort_by == "rating_desc":
            query = query.order_by(Product.average_rating.desc())
        elif sort_by == "newest":
            query = query.order_by(Product.created_at.desc())
        else:
            query = query.order_by(Product.id.desc())
            
        # Phân trang
        items = query.offset(skip).limit(limit).all()
        return items, total

product_repo = ProductRepository(Product)
