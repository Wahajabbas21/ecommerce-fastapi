from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.deps import get_db
from app.api.v1 import auth, users, products, orders, carts, inventory 
from app.api.v1 import admin
from app.api.v1 import dashboard
from app.api.v1 import chat

api_router = APIRouter()

# Registering individual feature routers with their respective URL prefixes and tags
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(carts.router, prefix="/cart", tags=["cart"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])

@api_router.get("/test")
def test_api():
    return {"message": "API v1 is working"}

@api_router.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {"status": "success", "message": "Database is connected!"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}