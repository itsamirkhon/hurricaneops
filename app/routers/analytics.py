from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.analytics import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard")
async def get_analytics_dashboard(db: Session = Depends(get_db)):
    return analytics_service.get_dashboard_stats(db)
