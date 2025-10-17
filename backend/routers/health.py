"""
Health check and system status endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Solar Predictive Maintenance System"
    }

@router.get("/healthcheck/db")
async def database_health_check(db: Session = Depends(get_db)):
    """
    Check database connectivity
    """
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/status")
async def system_status(db: Session = Depends(get_db)):
    """
    Get system status and statistics
    """
    from backend.models import SensorReading, Prediction, MaintenanceAlert
    
    try:
        total_readings = db.query(SensorReading).count()
        total_predictions = db.query(Prediction).count()
        open_alerts = db.query(MaintenanceAlert).filter(MaintenanceAlert.status == "open").count()
        
        return {
            "status": "operational",
            "statistics": {
                "total_sensor_readings": total_readings,
                "total_predictions": total_predictions,
                "open_maintenance_alerts": open_alerts
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
