from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.category_repo import category_repo
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.slug import generate_slug

class CategoryService:
    def create_category(self, db: Session, category_in: CategoryCreate):
        if not category_in.slug:
            category_in.slug = generate_slug(category_in.name)
        
        # Check if slug exists
        existing = category_repo.get_by_slug(db, slug=category_in.slug)
        if existing:
            raise HTTPException(status_code=400, detail="Category slug already exists")
            
        return category_repo.create(db, obj_in=category_in)

    def update_category(self, db: Session, category_id: int, category_in: CategoryUpdate):
        category = category_repo.get(db, id=category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
            
        if category_in.slug:
            existing = category_repo.get_by_slug(db, slug=category_in.slug)
            if existing and existing.id != category_id:
                raise HTTPException(status_code=400, detail="Category slug already exists")
                
        return category_repo.update(db, db_obj=category, obj_in=category_in)

    def get_category(self, db: Session, category_id: int):
        category = category_repo.get(db, id=category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
        
    def get_category_by_slug(self, db: Session, slug: str):
        category = category_repo.get_by_slug(db, slug=slug)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

category_service = CategoryService()
