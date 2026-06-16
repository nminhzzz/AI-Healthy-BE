from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.product_repo import product_repo
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.slug import generate_slug

class ProductService:
    def create_product(self, db: Session, product_in: ProductCreate):
        if not product_in.slug:
            product_in.slug = generate_slug(product_in.name)
            
        # Check slug
        existing_slug = product_repo.get_by_slug(db, slug=product_in.slug)
        if existing_slug:
            raise HTTPException(status_code=400, detail="Product slug already exists")
            
        # Check sku
        existing_sku = product_repo.get_by_sku(db, sku=product_in.sku)
        if existing_sku:
            raise HTTPException(status_code=400, detail="Product sku already exists")

        return product_repo.create(db, obj_in=product_in)

    def update_product(self, db: Session, product_id: int, product_in: ProductUpdate):
        product = product_repo.get(db, id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product_in.slug:
            existing = product_repo.get_by_slug(db, slug=product_in.slug)
            if existing and existing.id != product_id:
                raise HTTPException(status_code=400, detail="Product slug already exists")

        if product_in.sku:
            existing = product_repo.get_by_sku(db, sku=product_in.sku)
            if existing and existing.id != product_id:
                raise HTTPException(status_code=400, detail="Product sku already exists")

        return product_repo.update(db, db_obj=product, obj_in=product_in)

    def get_product(self, db: Session, product_id: int):
        product = product_repo.get(db, id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def get_product_by_slug(self, db: Session, slug: str):
        product = product_repo.get_by_slug(db, slug=slug)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

product_service = ProductService()
