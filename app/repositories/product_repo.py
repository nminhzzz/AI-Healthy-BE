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
        is_active: Optional[bool] = None
    ) -> List[Product]:
        query = db.query(Product)
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        if search_query:
            query = query.filter(Product.name.ilike(f"%{search_query}%"))
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
            
        return query.offset(skip).limit(limit).all()

product_repo = ProductRepository(Product)
