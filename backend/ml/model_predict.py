"""
ML Model Prediction and Inference
"""
import numpy as np
import joblib
import os
from typing import Dict
from backend.core.config import settings
from backend.core.utils import calculate_efficiency_loss, get_maintenance_priority, log_warning
from backend.ml.feature_engineering import prepare_single_prediction

# Global model and scaler cache
_model = None
_scaler = None

def load_model():
    """
    Load trained model and scaler (cached)
    """
    global _model, _scaler
    
    if _model is None or _scaler is None:
        model_path = 'backend/ml/models/solar_prediction_model.joblib'
        scaler_path = 'backend/ml/models/feature_scaler.joblib'
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            log_warning("Model files not found. Using fallback physics-based prediction.")
            return None, None
        
        _model = joblib.load(model_path)
        _scaler = joblib.load(scaler_path)
    
    return _model, _scaler

def physics_based_prediction(sensor_data) -> float:
    """
    Fallback: Physics-based prediction when ML model unavailable
    """
    # Base power from irradiance
    base_power = sensor_data.irradiance * 4.0
    
    # Apply degradation factors
    dust_loss = (sensor_data.pm10 * 0.0015 + sensor_data.pm25 * 0.002)
    temp_loss = max(0, (sensor_data.temperature - 25) * 0.004)
    humidity_factor = 1 - (sensor_data.humidity - 50) * 0.0005
    
    total_loss = (dust_loss + temp_loss) / 100
    predicted_power = base_power * (1 - total_loss) * humidity_factor
    
    return max(0, predicted_power)

def predict_performance(sensor_reading) -> Dict:
    """
    Predict solar panel performance and generate maintenance insights
    
    Args:
        sensor_reading: SensorReading model instance
    
    Returns:
        Dictionary with prediction results
    """
    # Load model
    model, scaler = load_model()
    
    # Prepare features
    features = prepare_single_prediction(sensor_reading)
    
    # Predict
    if model is not None and scaler is not None:
        features_scaled = scaler.transform([features])
        predicted_output = model.predict(features_scaled)[0]
    else:
        # Fallback to physics-based
        predicted_output = physics_based_prediction(sensor_reading)
    
    # Calculate degradation score
    actual_output = sensor_reading.power_output
    degradation_score = calculate_efficiency_loss(actual_output, predicted_output)
    
    # Determine if cleaning is needed
    cleaning_alert = degradation_score > settings.DEGRADATION_THRESHOLD
    maintenance_priority = get_maintenance_priority(degradation_score)
    
    return {
        'panel_id': sensor_reading.panel_id,
        'predicted_output': round(predicted_output, 2),
        'actual_output': round(actual_output, 2),
        'degradation_score': round(degradation_score, 2),
        'cleaning_alert': cleaning_alert,
        'maintenance_priority': maintenance_priority
    }

def batch_predict(sensor_readings):
    """
    Predict performance for multiple sensor readings
    
    Args:
        sensor_readings: List of SensorReading instances
    
    Returns:
        List of prediction dictionaries
    """
    return [predict_performance(reading) for reading in sensor_readings]
