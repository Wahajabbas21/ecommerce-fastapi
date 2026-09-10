from pydantic import BaseModel
from typing import List, Optional

class ProductInCart(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
    stock: int

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: Optional[ProductInCart] = None 

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]

    class Config:
        from_attributes = True