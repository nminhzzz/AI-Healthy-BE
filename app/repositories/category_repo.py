from sqlalchemy.orm import Session
from app.models.category import Category
from app.repositories.base import BaseRepository
from app.schemas.category import CategoryCreate, CategoryUpdate

class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def get_by_slug(self, db: Session, slug: str) -> Category | None:
        return db.query(Category).filter(Category.slug == slug).first()

category_repo = CategoryRepository(Category)
