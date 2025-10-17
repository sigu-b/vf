"""
Simulator Configuration
"""

# API Configuration
API_BASE_URL = "http://localhost:8000"
SENSOR_UPLOAD_ENDPOINT = "/api/sensor/upload"

# Simulation Parameters
SIMULATION_INTERVAL = 5  # seconds between readings
PANELS = ["panel_001", "panel_002", "panel_003"]

# Panel Specifications
PANEL_RATED_POWER = 4000  # Watts
PANEL_EFFICIENCY = 0.20
PANEL_AREA = 20  # m²

# Environmental Ranges (Nairobi/Kenya region)
PM10_BASE = 80  # μg/m³ (dry season baseline)
PM10_VARIATION = 100
PM25_BASE = 40
PM25_VARIATION = 50

TEMP_MIN = 15  # °C
TEMP_MAX = 35
TEMP_DAY_PEAK = 30

HUMIDITY_MIN = 30  # %
HUMIDITY_MAX = 70
HUMIDITY_NIGHT = 65

IRRADIANCE_MAX = 1000  # W/m² (clear day)
IRRADIANCE_CLOUDY = 200

# Dust Accumulation Model
DUST_ACCUMULATION_RATE = 2.0  # μg/m³ per day (dry season)
RAIN_PROBABILITY = 0.1  # 10% chance per day (dry season)
RAIN_CLEANING_FACTOR = 0.7  # 70% dust removed by rain

# Performance Degradation
DUST_IMPACT_FACTOR = 0.0015  # % power loss per μg/m³ PM10
TEMP_IMPACT_FACTOR = 0.004   # % power loss per °C above 25°C
