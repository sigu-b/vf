"""
Application configuration and environment variables
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Application
    APP_NAME: str = "Solar Predictive Maintenance System"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/solar_maintenance"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # ML Model
    MODEL_PATH: str = "backend/ml/models/solar_prediction_model.joblib"
    DEGRADATION_THRESHOLD: float = 15.0  # Alert if degradation > 15%
    CLEANING_THRESHOLD: float = 25.0     # Critical cleaning if > 25%
    
    # API Configuration
    API_V1_PREFIX: str = "/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
