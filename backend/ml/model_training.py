"""
ML Model Training for Solar Panel Performance Prediction
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from datetime import datetime
from backend.core.utils import log_info
from backend.ml.feature_engineering import prepare_features

def generate_synthetic_training_data(n_samples=10000):
    """
    Generate synthetic training data for model development
    Based on physics model and real-world correlations
    """
    np.random.seed(42)
    
    # Generate environmental features
    pm10 = np.random.uniform(20, 300, n_samples)
    pm25 = np.random.uniform(10, 150, n_samples)
    temperature = np.random.uniform(15, 45, n_samples)
    humidity = np.random.uniform(20, 80, n_samples)
    irradiance = np.random.uniform(100, 1200, n_samples)
    
    # Base power calculation (physics-based)
    base_power = irradiance * 4.0  # Simplified: 1000 W/m² → 4000W
    
    # Apply degradation factors
    dust_loss = pm10 * 0.0015 + pm25 * 0.002  # % loss per μg/m³
    temp_loss = np.maximum(0, (temperature - 25) * 0.004)  # Loss above 25°C
    humidity_factor = 1 - (humidity - 50) * 0.0005  # Slight impact
    
    # Calculate actual power with noise
    total_loss = (dust_loss + temp_loss) / 100
    power_output = base_power * (1 - total_loss) * humidity_factor
    power_output = power_output + np.random.normal(0, 50, n_samples)  # Add noise
    power_output = np.clip(power_output, 0, 5000)
    
    # Create DataFrame
    df = pd.DataFrame({
        'pm10': pm10,
        'pm25': pm25,
        'temperature': temperature,
        'humidity': humidity,
        'irradiance': irradiance,
        'power_output': power_output
    })
    
    return df

def train_model(data=None, model_type='random_forest'):
    """
    Train ML model to predict solar panel power output
    
    Args:
        data: Training data (if None, generates synthetic data)
        model_type: 'random_forest' or 'gradient_boosting'
    
    Returns:
        Trained model and scaler
    """
    log_info("Starting model training...")
    
    # Get training data
    if data is None:
        log_info("Generating synthetic training data...")
        data = generate_synthetic_training_data()
    
    # Prepare features
    X, y, feature_names = prepare_features(data)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Select and train model
    if model_type == 'random_forest':
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
    else:  # gradient_boosting
        model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
    
    log_info(f"Training {model_type} model...")
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    train_pred = model.predict(X_train_scaled)
    test_pred = model.predict(X_test_scaled)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    test_mae = mean_absolute_error(y_test, test_pred)
    
    log_info(f"Training RMSE: {train_rmse:.2f} W")
    log_info(f"Testing RMSE: {test_rmse:.2f} W")
    log_info(f"Training R²: {train_r2:.4f}")
    log_info(f"Testing R²: {test_r2:.4f}")
    log_info(f"Testing MAE: {test_mae:.2f} W")
    
    # Feature importance
    if hasattr(model, 'feature_importances_'):
        importances = sorted(
            zip(feature_names, model.feature_importances_),
            key=lambda x: x[1],
            reverse=True
        )
        log_info("Top 3 Feature Importances:")
        for feat, imp in importances[:3]:
            log_info(f"  {feat}: {imp:.4f}")
    
    return model, scaler, {
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'test_mae': test_mae,
        'model_type': model_type,
        'training_date': datetime.now().isoformat()
    }

def save_model(model, scaler, metrics, model_path='backend/ml/models/'):
    """
    Save trained model and scaler to disk
    """
    os.makedirs(model_path, exist_ok=True)
    
    model_file = os.path.join(model_path, 'solar_prediction_model.joblib')
    scaler_file = os.path.join(model_path, 'feature_scaler.joblib')
    metrics_file = os.path.join(model_path, 'model_metrics.joblib')
    
    joblib.dump(model, model_file)
    joblib.dump(scaler, scaler_file)
    joblib.dump(metrics, metrics_file)
    
    log_info(f"Model saved to {model_file}")
    log_info(f"Scaler saved to {scaler_file}")
    log_info(f"Metrics saved to {metrics_file}")

if __name__ == "__main__":
    # Train and save model
    model, scaler, metrics = train_model(model_type='random_forest')
    save_model(model, scaler, metrics)
    print("\nModel training completed successfully!")
    print(f"Test R² Score: {metrics['test_r2']:.4f}")
    print(f"Test RMSE: {metrics['test_rmse']:.2f} W")
