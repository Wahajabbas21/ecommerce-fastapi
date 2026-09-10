from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.dashboard import DashboardMetrics
from app.services import dashboard_service
from app.api.v1.admin import verify_admin 

router = APIRouter()

@router.get("/", response_model=DashboardMetrics)
def get_dashboard_data(
    db: Session = Depends(get_db),
    admin_user = Depends(verify_admin)
):
    """Admin endpoint: Dashboard ke liye aggregate metrics return karega."""
    return dashboard_service.get_dashboard_metrics(db=db)