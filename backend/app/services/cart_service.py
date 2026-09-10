from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate

def get_or_create_cart(db: Session, user_id: int) -> Cart:
    # joinedload use kiya hai taake Cart ke sath items aur products ek hi query mein aa jayein
    cart = db.query(Cart).options(
        joinedload(Cart.items).joinedload(CartItem.product)
    ).filter(Cart.user_id == user_id).first()
    
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        # Nayi cart ke liye dobara eager load karke return karna
        cart = db.query(Cart).options(
            joinedload(Cart.items).joinedload(CartItem.product)
        ).filter(Cart.id == cart.id).first()
        
    return cart

def add_item_to_cart(db: Session, user_id: int, item_in: CartItemCreate) -> Cart:
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {item_in.product_id} not found"
        )
    
    if product.stock < item_in.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock available for product: {product.name}"
        )

    cart = get_or_create_cart(db, user_id)

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_in.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item_in.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity
        )
        db.add(cart_item)

    db.commit()
    return get_or_create_cart(db, user_id)

def get_user_cart(db: Session, user_id: int) -> Cart:
    return get_or_create_cart(db, user_id)

def update_cart_item_quantity(db: Session, user_id: int, item_id: int, quantity: int) -> Cart:
    cart = get_or_create_cart(db, user_id)
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if product.stock < quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock available")
    
    cart_item.quantity = quantity
    db.commit()
    return get_or_create_cart(db, user_id)

def remove_item_from_cart(db: Session, user_id: int, item_id: int) -> Cart:
    cart = get_or_create_cart(db, user_id)
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return get_or_create_cart(db, user_id)

def clear_cart(db: Session, user_id: int) -> Cart:
    cart = get_or_create_cart(db, user_id)
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return get_or_create_cart(db, user_id)