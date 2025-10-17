"""
Sensor data ingestion endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend import crud, schemas
from backend.database import get_db
from backend.core.utils import log_info

router = APIRouter()

@router.post("/upload", response_model=schemas.SensorReadingResponse, status_code=status.HTTP_201_CREATED)
async def upload_sensor_data(
    reading: schemas.SensorReadingCreate,
    db: Session = Depends(get_db)
):
    """
    Upload sensor reading from IoT device or simulator
    
    - **panel_id**: Unique panel identifier
    - **pm10**: PM10 concentration (μg/m³)
    - **pm25**: PM2.5 concentration (μg/m³)
    - **temperature**: Temperature (°C)
    - **humidity**: Relative humidity (%)
    - **irradiance**: Solar irradiance (W/m²)
    - **power_output**: Actual power output (W)
    """
    try:
        db_reading = crud.create_sensor_reading(db, reading)
        log_info(f"Sensor data uploaded for panel {reading.panel_id}")
        return db_reading
    except Exception as e:
        log_info(f"Error uploading sensor data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store sensor reading: {str(e)}"
        )

@router.get("/readings", response_model=List[schemas.SensorReadingResponse])
async def get_sensor_readings(
    panel_id: str = None,
    hours: int = 24,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve sensor readings with optional filters
    
    - **panel_id**: Filter by specific panel (optional)
    - **hours**: Get readings from last N hours (default: 24)
    - **limit**: Maximum number of records (default: 100)
    """
    readings = crud.get_sensor_readings(db, panel_id=panel_id, hours=hours, limit=limit)
    return readings

@router.get("/readings/latest/{panel_id}", response_model=schemas.SensorReadingResponse)
async def get_latest_reading(
    panel_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the most recent sensor reading for a specific panel
    """
    reading = crud.get_latest_reading(db, panel_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No readings found for panel {panel_id}"
        )
    return reading
