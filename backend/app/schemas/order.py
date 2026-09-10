from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float  
    status: str
    shipping_address: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
    
class OrderStatusUpdate(BaseModel):
    status: str