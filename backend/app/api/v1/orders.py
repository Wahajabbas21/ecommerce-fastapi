from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.api.deps import get_db, get_current_user
from app.schemas.order import OrderResponse
from app.services import order_service
from app.models.user import User
from app.models.order import Order

router = APIRouter()

class OrderCreate(BaseModel):
    shipping_address: str
    phone_number: str

class OrderStatusUpdate(BaseModel):
    status: str

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return order_service.create_order(
            db=db, 
            user_id=current_user.id, 
            shipping_address=order_in.shipping_address, 
            phone_number=order_in.phone_number
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[OrderResponse])
def read_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_service.get_user_orders(db=db, user_id=current_user.id)

@router.get("/{order_id}", response_model=OrderResponse)
def read_user_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_service.get_user_order_by_id(db=db, user_id=current_user.id, order_id=order_id)

# ==================== ADMIN ENDPOINTS ====================

@router.get("/admin/all", response_model=List[OrderResponse])
def get_all_admin_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).offset(skip).limit(limit).all()

@router.patch("/admin/{order_id}/status", response_model=OrderResponse)
def update_order_status_admin(
    order_id: int, 
    status_update: OrderStatusUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order