"""
Pydantic schemas for data validation and serialization
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

# ============ Sensor Readings ============

class SensorReadingBase(BaseModel):
    panel_id: str = Field(..., description="Unique panel identifier")
    pm10: float = Field(..., ge=0, description="PM10 concentration (μg/m³)")
    pm25: float = Field(..., ge=0, description="PM2.5 concentration (μg/m³)")
    temperature: float = Field(..., ge=-50, le=100, description="Temperature (°C)")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity (%)")
    irradiance: float = Field(..., ge=0, le=1500, description="Solar irradiance (W/m²)")
    power_output: float = Field(..., ge=0, description="Power output (W)")

class SensorReadingCreate(SensorReadingBase):
    timestamp: Optional[datetime] = None

class SensorReadingResponse(SensorReadingBase):
    id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Predictions ============

class PredictionBase(BaseModel):
    panel_id: str
    predicted_output: float
    actual_output: Optional[float] = None
    degradation_score: float = Field(..., ge=0, le=100)
    cleaning_alert: bool = False
    maintenance_priority: str = "normal"

class PredictionCreate(PredictionBase):
    pass

class PredictionResponse(PredictionBase):
    id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Maintenance Alerts ============

class MaintenanceAlertBase(BaseModel):
    panel_id: str
    alert_type: str = Field(..., description="Type: cleaning, inspection, repair")
    priority: str = "normal"
    message: str
    estimated_days_until_critical: Optional[int] = None

class MaintenanceAlertCreate(MaintenanceAlertBase):
    pass

class MaintenanceAlertResponse(MaintenanceAlertBase):
    id: int
    timestamp: datetime
    status: str
    resolved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Analytics Responses ============

class AnalyticsSummary(BaseModel):
    panel_id: str
    total_readings: int
    avg_power_output: float
    avg_degradation_score: float
    active_alerts: int
    last_reading_time: Optional[datetime] = None

class PerformanceTrend(BaseModel):
    timestamp: datetime
    power_output: float
    predicted_output: Optional[float] = None
    degradation_score: Optional[float] = None
