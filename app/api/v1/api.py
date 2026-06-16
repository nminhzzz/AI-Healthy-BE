from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1.admin import categories as admin_categories
from app.api.v1.admin import products as admin_products
from app.api.v1.admin import users as admin_users
from app.api.v1 import categories as public_categories
from app.api.v1 import products as public_products
from app.api.v1 import reviews as public_reviews
from app.api.v1.endpoints import upload

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Admin routes
api_router.include_router(admin_categories.router, prefix="/admin/categories", tags=["Admin - Categories"])
api_router.include_router(admin_products.router, prefix="/admin/products", tags=["Admin - Products"])
api_router.include_router(admin_users.router, prefix="/admin/users", tags=["Admin - Users"])

# Public routes
api_router.include_router(public_categories.router, prefix="/categories", tags=["Public - Categories"])
api_router.include_router(public_products.router, prefix="/products", tags=["Public - Products"])
api_router.include_router(public_reviews.router, prefix="/reviews", tags=["Public - Reviews"])

# Upload routes
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
