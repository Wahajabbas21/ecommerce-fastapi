from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from app.services import cart_service

router = APIRouter()

@router.post("/", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item_in: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.add_item_to_cart(db=db, user_id=current_user.id, item_in=item_in)

@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.get_user_cart(db=db, user_id=current_user.id)

@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: int,
    item_in: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.update_cart_item_quantity(db=db, user_id=current_user.id, item_id=item_id, quantity=item_in.quantity)

@router.delete("/items/{item_id}", response_model=CartResponse)
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.remove_item_from_cart(db=db, user_id=current_user.id, item_id=item_id)

@router.delete("/", response_model=CartResponse)
def clear_cart_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.clear_cart(db=db, user_id=current_user.id)