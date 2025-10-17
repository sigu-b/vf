"""
Feature engineering for ML models
"""
import numpy as np
import pandas as pd

def prepare_features(data):
    """
    Prepare features for model training
    
    Args:
        data: DataFrame with sensor data
    
    Returns:
        X (features), y (target), feature_names
    """
    # Base features
    feature_cols = ['pm10', 'pm25', 'temperature', 'humidity', 'irradiance']
    
    # Create engineered features
    df = data.copy()
    
    # Interaction features
    df['dust_total'] = df['pm10'] + df['pm25']
    df['dust_ratio'] = df['pm25'] / (df['pm10'] + 1)  # Avoid division by zero
    df['temp_irradiance'] = df['temperature'] * df['irradiance']
    df['humidity_temp'] = df['humidity'] * df['temperature']
    
    # Polynomial features (squared terms for key variables)
    df['pm10_squared'] = df['pm10'] ** 2
    df['temperature_squared'] = df['temperature'] ** 2
    
    # Temperature deviation from optimal (25°C)
    df['temp_deviation'] = np.abs(df['temperature'] - 25)
    
    # All feature columns
    feature_names = [
        'pm10', 'pm25', 'temperature', 'humidity', 'irradiance',
        'dust_total', 'dust_ratio', 'temp_irradiance', 'humidity_temp',
        'pm10_squared', 'temperature_squared', 'temp_deviation'
    ]
    
    X = df[feature_names].values
    y = df['power_output'].values
    
    return X, y, feature_names

def prepare_single_prediction(sensor_reading):
    """
    Prepare features for a single prediction
    
    Args:
        sensor_reading: SensorReading model instance
    
    Returns:
        Feature array for prediction
    """
    # Extract base features
    pm10 = sensor_reading.pm10
    pm25 = sensor_reading.pm25
    temperature = sensor_reading.temperature
    humidity = sensor_reading.humidity
    irradiance = sensor_reading.irradiance
    
    # Engineer features (same as training)
    dust_total = pm10 + pm25
    dust_ratio = pm25 / (pm10 + 1)
    temp_irradiance = temperature * irradiance
    humidity_temp = humidity * temperature
    pm10_squared = pm10 ** 2
    temperature_squared = temperature ** 2
    temp_deviation = abs(temperature - 25)
    
    # Return in same order as training
    return [
        pm10, pm25, temperature, humidity, irradiance,
        dust_total, dust_ratio, temp_irradiance, humidity_temp,
        pm10_squared, temperature_squared, temp_deviation
    ]
