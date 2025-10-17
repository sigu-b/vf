"""
Analytics and prediction endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import crud, schemas
from backend.database import get_db
from backend.ml.model_predict import predict_performance
from backend.core.utils import log_info

router = APIRouter()

@router.get("/summary/{panel_id}", response_model=schemas.AnalyticsSummary)
async def get_analytics_summary(
    panel_id: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """
    Get analytics summary for a specific panel
    
    - **panel_id**: Panel identifier
    - **hours**: Analysis window in hours (default: 24)
    """
    summary = crud.get_panel_analytics(db, panel_id, hours)
    return summary

@router.get("/predictions", response_model=List[schemas.PredictionResponse])
async def get_predictions(
    panel_id: str = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve ML predictions
    
    - **panel_id**: Filter by specific panel (optional)
    - **limit**: Maximum number of records (default: 100)
    """
    predictions = crud.get_predictions(db, panel_id=panel_id, limit=limit)
    return predictions

@router.post("/predict/{panel_id}", response_model=schemas.PredictionResponse)
async def create_prediction(
    panel_id: str,
    db: Session = Depends(get_db)
):
    """
    Generate prediction for a panel based on latest sensor data
    
    - **panel_id**: Panel identifier
    """
    # Get latest sensor reading
    reading = crud.get_latest_reading(db, panel_id)
    if not reading:
        raise HTTPException(
            status_code=404,
            detail=f"No sensor data found for panel {panel_id}"
        )
    
    # Generate prediction
    try:
        prediction_data = predict_performance(reading)
        db_prediction = crud.create_prediction(db, schemas.PredictionCreate(**prediction_data))
        
        log_info(f"Prediction generated for panel {panel_id}: degradation={prediction_data['degradation_score']:.2f}%")
        
        return db_prediction
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@router.get("/trend/{panel_id}", response_model=List[schemas.PerformanceTrend])
async def get_performance_trend(
    panel_id: str,
    hours: int = 168,  # 7 days default
    db: Session = Depends(get_db)
):
    """
    Get performance trend data for visualization
    
    - **panel_id**: Panel identifier
    - **hours**: Time window in hours (default: 168 = 7 days)
    """
    # Get sensor readings
    readings = crud.get_sensor_readings(db, panel_id=panel_id, hours=hours, limit=1000)
    
    # Get predictions
    predictions = crud.get_predictions(db, panel_id=panel_id, limit=1000)
    
    # Merge data for trend
    trend_data = []
    pred_dict = {p.timestamp: p for p in predictions}
    
    for reading in readings:
        pred = pred_dict.get(reading.timestamp)
        trend_data.append({
            "timestamp": reading.timestamp,
            "power_output": reading.power_output,
            "predicted_output": pred.predicted_output if pred else None,
            "degradation_score": pred.degradation_score if pred else None
        })
    
    return trend_data
