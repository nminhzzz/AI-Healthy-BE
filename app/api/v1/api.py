from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1.admin import categories as admin_categories
from app.api.v1.admin import products as admin_products
from app.api.v1 import categories as public_categories
from app.api.v1 import products as public_products
from app.api.v1 import reviews as public_reviews

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Admin routes
api_router.include_router(admin_categories.router, prefix="/admin/categories", tags=["Admin - Categories"])
api_router.include_router(admin_products.router, prefix="/admin/products", tags=["Admin - Products"])

# Public routes
api_router.include_router(public_categories.router, prefix="/categories", tags=["Public - Categories"])
api_router.include_router(public_products.router, prefix="/products", tags=["Public - Products"])
api_router.include_router(public_reviews.router, prefix="/reviews", tags=["Public - Reviews"])
