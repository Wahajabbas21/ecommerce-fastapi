from pydantic import BaseModel
from typing import Dict

class DashboardMetrics(BaseModel):
    total_customers: int
    total_orders: int
    pending_orders: int
    total_sales: float
    orders_by_status: Dict[str, int]