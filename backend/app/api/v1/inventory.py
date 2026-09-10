from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.product import Product
from app.schemas.inventory import InventoryResponse

router = APIRouter()

@router.get("/", response_model=List[InventoryResponse])
def get_inventory(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve inventory records based on the Product model 
    validated through the InventoryResponse schema.
    """
    products = db.query(Product).all()
    return products