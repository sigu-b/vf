"""
CRUD (Create, Read, Update, Delete) operations for database
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from typing import List, Optional
from backend import models, schemas

# ============ Sensor Readings ============

def create_sensor_reading(db: Session, reading: schemas.SensorReadingCreate) -> models.SensorReading:
    """Create a new sensor reading"""
    db_reading = models.SensorReading(**reading.model_dump())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

def get_sensor_readings(
    db: Session,
    panel_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    hours: Optional[int] = None
) -> List[models.SensorReading]:
    """Get sensor readings with optional filtering"""
    query = db.query(models.SensorReading)
    
    if panel_id:
        query = query.filter(models.SensorReading.panel_id == panel_id)
    
    if hours:
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(models.SensorReading.timestamp >= time_threshold)
    
    return query.order_by(desc(models.SensorReading.timestamp)).offset(skip).limit(limit).all()

def get_latest_reading(db: Session, panel_id: str) -> Optional[models.SensorReading]:
    """Get the most recent reading for a panel"""
    return db.query(models.SensorReading)\
        .filter(models.SensorReading.panel_id == panel_id)\
        .order_by(desc(models.SensorReading.timestamp))\
        .first()

# ============ Predictions ============

def create_prediction(db: Session, prediction: schemas.PredictionCreate) -> models.Prediction:
    """Create a new prediction record"""
    db_prediction = models.Prediction(**prediction.model_dump())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def get_predictions(
    db: Session,
    panel_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.Prediction]:
    """Get predictions with optional filtering"""
    query = db.query(models.Prediction)
    
    if panel_id:
        query = query.filter(models.Prediction.panel_id == panel_id)
    
    return query.order_by(desc(models.Prediction.timestamp)).offset(skip).limit(limit).all()

# ============ Maintenance Alerts ============

def create_alert(db: Session, alert: schemas.MaintenanceAlertCreate) -> models.MaintenanceAlert:
    """Create a new maintenance alert"""
    db_alert = models.MaintenanceAlert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alerts(
    db: Session,
    panel_id: Optional[str] = None,
    status: Optional[str] = "open",
    skip: int = 0,
    limit: int = 100
) -> List[models.MaintenanceAlert]:
    """Get maintenance alerts with filtering"""
    query = db.query(models.MaintenanceAlert)
    
    if panel_id:
        query = query.filter(models.MaintenanceAlert.panel_id == panel_id)
    
    if status:
        query = query.filter(models.MaintenanceAlert.status == status)
    
    return query.order_by(desc(models.MaintenanceAlert.timestamp)).offset(skip).limit(limit).all()

def update_alert_status(db: Session, alert_id: int, status: str) -> Optional[models.MaintenanceAlert]:
    """Update alert status"""
    alert = db.query(models.MaintenanceAlert).filter(models.MaintenanceAlert.id == alert_id).first()
    if alert:
        alert.status = status
        if status == "resolved":
            alert.resolved_at = datetime.utcnow()
        db.commit()
        db.refresh(alert)
    return alert

# ============ Analytics ============

def get_panel_analytics(db: Session, panel_id: str, hours: int = 24) -> dict:
    """Get analytics summary for a panel"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    # Get sensor reading stats
    readings = db.query(models.SensorReading)\
        .filter(
            models.SensorReading.panel_id == panel_id,
            models.SensorReading.timestamp >= time_threshold
        ).all()
    
    # Get prediction stats
    predictions = db.query(models.Prediction)\
        .filter(
            models.Prediction.panel_id == panel_id,
            models.Prediction.timestamp >= time_threshold
        ).all()
    
    # Get active alerts
    active_alerts = db.query(models.MaintenanceAlert)\
        .filter(
            models.MaintenanceAlert.panel_id == panel_id,
            models.MaintenanceAlert.status == "open"
        ).count()
    
    avg_power = sum(r.power_output for r in readings) / len(readings) if readings else 0
    avg_degradation = sum(p.degradation_score for p in predictions) / len(predictions) if predictions else 0
    
    return {
        "panel_id": panel_id,
        "total_readings": len(readings),
        "avg_power_output": round(avg_power, 2),
        "avg_degradation_score": round(avg_degradation, 2),
        "active_alerts": active_alerts,
        "last_reading_time": readings[0].timestamp if readings else None
    }
