"""
Maintenance alert endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend import crud, schemas
from backend.database import get_db
from backend.core.utils import log_info

router = APIRouter()

@router.post("/", response_model=schemas.MaintenanceAlertResponse, status_code=status.HTTP_201_CREATED)
async def create_maintenance_alert(
    alert: schemas.MaintenanceAlertCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new maintenance alert
    
    - **panel_id**: Panel identifier
    - **alert_type**: Type (cleaning, inspection, repair)
    - **priority**: Priority level (low, normal, high, critical)
    - **message**: Alert description
    """
    db_alert = crud.create_alert(db, alert)
    log_info(f"Alert created for panel {alert.panel_id}: {alert.alert_type} - {alert.priority}")
    return db_alert

@router.get("/", response_model=List[schemas.MaintenanceAlertResponse])
async def get_maintenance_alerts(
    panel_id: str = None,
    status: str = "open",
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve maintenance alerts
    
    - **panel_id**: Filter by panel (optional)
    - **status**: Filter by status (open, acknowledged, resolved)
    - **limit**: Maximum number of records
    """
    alerts = crud.get_alerts(db, panel_id=panel_id, status=status, limit=limit)
    return alerts

@router.patch("/{alert_id}/status")
async def update_alert_status(
    alert_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):
    """
    Update alert status
    
    - **alert_id**: Alert identifier
    - **new_status**: New status (acknowledged, resolved)
    """
    if new_status not in ["open", "acknowledged", "resolved"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Must be: open, acknowledged, or resolved"
        )
    
    alert = crud.update_alert_status(db, alert_id, new_status)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found"
        )
    
    log_info(f"Alert {alert_id} status updated to {new_status}")
    return {"message": "Alert status updated", "alert_id": alert_id, "status": new_status}
