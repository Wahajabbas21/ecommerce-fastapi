from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.order import Order
from typing import List

# State Machine: Allowed status transitions
ALLOWED_TRANSITIONS = {
    "Pending": ["Confirmed", "Cancelled"],
    "Confirmed": ["Processing"],
    "Processing": ["Shipped"],
    "Shipped": ["Delivered"],
    "Delivered": [],
    "Cancelled": []
}

def get_all_orders(db: Session) -> List[Order]:
    # Admin ke liye tamam users ke orders descend order mein laane ka query
    return db.query(Order).order_by(Order.id.desc()).all()

def update_order_status(db: Session, order_id: int, new_status: str) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    current_status = order.status
    
    # Validation: Ensure transition is allowed
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, []):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid transition from {current_status} to {new_status}"
        )
        
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order