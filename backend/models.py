"""
SQLAlchemy ORM models for database tables
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.sql import func
from backend.database import Base

class SensorReading(Base):
    """
    Stores sensor readings from solar panels
    """
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Environmental sensors
    pm10 = Column(Float, nullable=False, comment="Particulate Matter 10μm (μg/m³)")
    pm25 = Column(Float, nullable=False, comment="Particulate Matter 2.5μm (μg/m³)")
    temperature = Column(Float, nullable=False, comment="Temperature (°C)")
    humidity = Column(Float, nullable=False, comment="Relative Humidity (%)")
    irradiance = Column(Float, nullable=False, comment="Solar Irradiance (W/m²)")
    
    # Power output
    power_output = Column(Float, nullable=False, comment="Actual Power Output (W)")
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Prediction(Base):
    """
    Stores ML model predictions for panel performance
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Prediction results
    predicted_output = Column(Float, nullable=False, comment="Predicted Power Output (W)")
    actual_output = Column(Float, nullable=True, comment="Actual Power Output (W)")
    degradation_score = Column(Float, nullable=False, comment="Performance Degradation Score (0-100)")
    
    # Alert flags
    cleaning_alert = Column(Boolean, default=False, comment="Cleaning Required Flag")
    maintenance_priority = Column(String, default="normal", comment="Priority: low, normal, high, critical")
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MaintenanceAlert(Base):
    """
    Stores maintenance alerts and recommendations
    """
    __tablename__ = "maintenance_alerts"

    id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    alert_type = Column(String, nullable=False, comment="Type: cleaning, inspection, repair")
    priority = Column(String, default="normal", comment="Priority level")
    message = Column(String, nullable=False)
    estimated_days_until_critical = Column(Integer, nullable=True)
    
    # Status tracking
    status = Column(String, default="open", comment="Status: open, acknowledged, resolved")
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
