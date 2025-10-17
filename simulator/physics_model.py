"""
Physics-based solar panel power calculation
"""
import math
from simulator.config import (
    PANEL_RATED_POWER,
    DUST_IMPACT_FACTOR,
    TEMP_IMPACT_FACTOR
)

def calculate_power_output(irradiance, temperature, pm10, pm25, humidity):
    """
    Calculate solar panel power output based on environmental conditions
    
    Args:
        irradiance: Solar irradiance (W/m²)
        temperature: Panel temperature (°C)
        pm10: PM10 dust concentration (μg/m³)
        pm25: PM2.5 dust concentration (μg/m³)
        humidity: Relative humidity (%)
    
    Returns:
        Power output (W)
    """
    # Base power from irradiance
    # Standard test conditions: 1000 W/m² → rated power
    base_power = (irradiance / 1000.0) * PANEL_RATED_POWER
    
    # Temperature coefficient (panels lose efficiency when hot)
    # Standard reference: 25°C
    temp_loss_percent = max(0, (temperature - 25) * TEMP_IMPACT_FACTOR)
    
    # Dust soiling loss
    # Research shows ~0.15% loss per 100 μg/m³ of PM10
    dust_loss_percent = (pm10 * DUST_IMPACT_FACTOR + pm25 * 0.002)
    
    # Humidity impact (minor)
    humidity_factor = 1.0 - (abs(humidity - 50) * 0.0005)
    
    # Calculate total loss
    total_efficiency = 1.0 - (temp_loss_percent + dust_loss_percent) / 100.0
    total_efficiency = max(0, min(1.0, total_efficiency))  # Clamp 0-1
    
    # Final power output
    power = base_power * total_efficiency * humidity_factor
    
    # Add small random variation (measurement noise, micro-shading, etc.)
    import random
    noise = random.gauss(0, power * 0.02)  # 2% standard deviation
    power = max(0, power + noise)
    
    return power
