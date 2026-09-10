from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.order import Order

def get_dashboard_metrics(db: Session):
    # 1. COUNT Logic
    total_customers = db.query(User).filter(getattr(User, "is_admin", False) == False).count()
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == "Pending").count()
    
    # 2. SUM Logic
    total_sales_result = db.query(func.sum(Order.total_price)).scalar()
    total_sales = float(total_sales_result) if total_sales_result else 0.0

    # 3. GROUPING Logic (Status ke hisaab se orders count karna)
    status_grouping = db.query(
        Order.status, 
        func.count(Order.id)
    ).group_by(Order.status).all()
    
    # List of tuples ko dictionary mein convert karna
    orders_by_status = {status: count for status, count in status_grouping}

    return {
        "total_customers": total_customers,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_sales": total_sales,
        "orders_by_status": orders_by_status
    }