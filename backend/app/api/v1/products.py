from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import (
    create_product, 
    get_products, 
    get_product_by_id, 
    update_product, 
    delete_product
)
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product_in: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return create_product(db=db, product_in=product_in)

# Naye routes yahan add karein:

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(
    product_id: int,
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = get_product_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return update_product(db=db, db_product=product, product_in=product_in)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = get_product_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    delete_product(db=db, product_id=product_id)
    return None