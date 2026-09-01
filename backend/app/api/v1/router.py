from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.deps import get_db

api_router = APIRouter()

@api_router.get("/test")
def test_api():
    return {
        "message": "API v1 is working"
    }

@api_router.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Ek simple query chala kar database connection test kar rahe hain
        result = db.execute(text("SELECT 1")).scalar()
        return {"status": "success", "db_result": result, "message": "Database is connected!"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
        