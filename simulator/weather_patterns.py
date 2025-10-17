"""
Realistic weather and environmental pattern simulation
"""
import math
import random
from datetime import datetime
from simulator.config import (
    TEMP_MIN, TEMP_MAX, TEMP_DAY_PEAK,
    HUMIDITY_MIN, HUMIDITY_MAX, HUMIDITY_NIGHT,
    IRRADIANCE_MAX, IRRADIANCE_CLOUDY,
    PM10_BASE, PM10_VARIATION,
    PM25_BASE, PM25_VARIATION,
    DUST_ACCUMULATION_RATE,
    RAIN_PROBABILITY, RAIN_CLEANING_FACTOR
)

class WeatherSimulator:
    """
    Simulates realistic diurnal and seasonal weather patterns
    """
    
    def __init__(self):
        self.dust_accumulation = 0  # Accumulated dust (μg/m³)
        self.last_rain = None
        self.is_cloudy = False
        
    def get_time_of_day_factor(self):
        """
        Get normalized time of day (0=midnight, 0.5=noon, 1=midnight)
        """
        now = datetime.now()
        hour = now.hour + now.minute / 60.0
        # Normalize to 0-1 (0=midnight, 0.5=noon)
        return hour / 24.0
    
    def calculate_solar_irradiance(self):
        """
        Calculate solar irradiance based on time of day
        Uses sinusoidal model for day/night cycle
        """
        time_factor = self.get_time_of_day_factor()
        
        # Sunrise ~6:30 AM (0.27), Sunset ~6:30 PM (0.77) for equatorial regions
        sunrise = 0.27
        sunset = 0.77
        
        if time_factor < sunrise or time_factor > sunset:
            # Night time
            return 0
        
        # Daytime: sinusoidal curve
        day_progress = (time_factor - sunrise) / (sunset - sunrise)
        irradiance = IRRADIANCE_MAX * math.sin(day_progress * math.pi)
        
        # Cloud cover variation
        if random.random() < 0.2:  # 20% chance of clouds
            self.is_cloudy = True
            irradiance *= random.uniform(0.2, 0.6)  # 20-60% of clear sky
        else:
            self.is_cloudy = False
        
        # Small random variations
        irradiance *= random.uniform(0.95, 1.05)
        
        return max(0, irradiance)
    
    def calculate_temperature(self):
        """
        Calculate temperature with diurnal variation
        """
        time_factor = self.get_time_of_day_factor()
        
        # Peak temperature around 2 PM (0.58)
        peak_time = 0.58
        
        # Sinusoidal temperature variation
        if time_factor < peak_time:
            # Morning: rising temperature
            temp_progress = time_factor / peak_time
            temp = TEMP_MIN + (TEMP_DAY_PEAK - TEMP_MIN) * (math.sin(temp_progress * math.pi / 2))
        else:
            # Afternoon/Evening: falling temperature
            temp_progress = (time_factor - peak_time) / (1 - peak_time)
            temp = TEMP_DAY_PEAK - (TEMP_DAY_PEAK - TEMP_MIN) * (math.sin(temp_progress * math.pi / 2))
        
        # Add small random variation
        temp += random.gauss(0, 2)
        
        return max(TEMP_MIN, min(TEMP_MAX, temp))
    
    def calculate_humidity(self):
        """
        Calculate relative humidity (inverse of temperature generally)
        """
        time_factor = self.get_time_of_day_factor()
        
        # Higher humidity at night/morning
        humidity = HUMIDITY_NIGHT - (HUMIDITY_NIGHT - HUMIDITY_MIN) * abs(math.sin(time_factor * 2 * math.pi))
        
        # Cloudy days have higher humidity
        if self.is_cloudy:
            humidity *= random.uniform(1.1, 1.3)
        
        humidity += random.gauss(0, 5)
        
        return max(HUMIDITY_MIN, min(HUMIDITY_MAX, humidity))
    
    def calculate_dust_levels(self):
        """
        Calculate PM10 and PM2.5 with accumulation over time
        """
        # Check for rain (cleaning event)
        if random.random() < RAIN_PROBABILITY / 24:  # Per hour probability
            self.dust_accumulation *= (1 - RAIN_CLEANING_FACTOR)
            self.last_rain = datetime.now()
        
        # Dust accumulates over time (more during day due to activity)
        time_factor = self.get_time_of_day_factor()
        if 0.25 < time_factor < 0.75:  # Daytime
            self.dust_accumulation += DUST_ACCUMULATION_RATE / 24  # Per hour
        
        # Current dust levels
        pm10 = PM10_BASE + self.dust_accumulation + random.uniform(0, PM10_VARIATION)
        pm25 = PM25_BASE + (self.dust_accumulation * 0.5) + random.uniform(0, PM25_VARIATION)
        
        # Windy conditions can reduce or increase dust
        if random.random() < 0.1:  # 10% chance of wind event
            wind_factor = random.uniform(0.7, 1.3)
            pm10 *= wind_factor
            pm25 *= wind_factor
        
        return max(0, pm10), max(0, pm25)
    
    def get_current_conditions(self):
        """
        Get all current environmental conditions
        """
        return {
            'irradiance': self.calculate_solar_irradiance(),
            'temperature': self.calculate_temperature(),
            'humidity': self.calculate_humidity(),
            'pm10': self.calculate_dust_levels()[0],
            'pm25': self.calculate_dust_levels()[1]
        }
