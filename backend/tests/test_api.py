"""
API endpoint tests
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Solar Predictive Maintenance" in data["message"]

def test_sensor_upload():
    """Test sensor data upload"""
    sensor_data = {
        "panel_id": "test_panel",
        "pm10": 120.5,
        "pm25": 65.3,
        "temperature": 32.5,
        "humidity": 45.2,
        "irradiance": 850.0,
        "power_output": 3420.5
    }
    
    response = client.post("/api/sensor/upload", json=sensor_data)
    assert response.status_code == 201
    data = response.json()
    assert data["panel_id"] == "test_panel"
    assert data["pm10"] == 120.5

def test_sensor_upload_invalid_data():
    """Test sensor upload with invalid data"""
    invalid_data = {
        "panel_id": "test_panel",
        "pm10": -50,  # Invalid negative value
        "temperature": 200  # Unrealistic temperature
    }
    
    response = client.post("/api/sensor/upload", json=invalid_data)
    assert response.status_code == 422  # Validation error
