from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.schemas.order import OrderResponse
from app.schemas.order import OrderStatusUpdate # Agar isi file mein banaya hy
from app.services import admin_service
from app.models.user import User

router = APIRouter()

# Dependency to block non-admin users
def verify_admin(current_user: User = Depends(get_current_user)):
    # Note: Agar aapke User model mein role ka column kisi aur naam se hai (e.g. role == "admin"), 
    # toh is condition ko us hisab se adjust kar lein.
    if not getattr(current_user, "is_admin", False): 
        raise HTTPException(status_code=403, detail="Not enough permissions. Admin only.")
    return current_user

@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders_admin(
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Admin endpoint: Tamam system orders ki list return karega."""
    return admin_service.get_all_orders(db=db)

@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status_admin(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Admin endpoint: Kisi order ka status update karne ke liye."""
    return admin_service.update_order_status(db=db, order_id=order_id, new_status=status_data.status)