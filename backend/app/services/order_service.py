from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product

def create_order(db: Session, user_id: int, shipping_address: str, phone_number: str):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0
    order_items_data = []

    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        item_price = product.price
        total_price += item_price * cart_item.quantity
        
        order_items_data.append({
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "price": item_price
        })

    db_order = Order(
        user_id=user_id,
        total_price=total_price,
        status="pending",
        shipping_address=shipping_address,
        phone_number=phone_number
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item_data in order_items_data:
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            price=item_data["price"]
        )
        db.add(db_order_item)

    for cart_item in cart.items:
        db.delete(cart_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_user_order_by_id(db: Session, user_id: int, order_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order