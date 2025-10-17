"""
Application constants and thresholds
"""

# Solar Panel Specifications
PANEL_RATED_POWER = 4000  # Watts (4kW panel)
PANEL_EFFICIENCY = 0.20    # 20% efficiency
PANEL_AREA = 20            # Square meters

# Environmental Thresholds
PM10_CRITICAL = 200        # μg/m³
PM25_CRITICAL = 100        # μg/m³
TEMP_OPTIMAL_MIN = 15      # °C
TEMP_OPTIMAL_MAX = 35      # °C
HUMIDITY_OPTIMAL_MAX = 60  # %

# Performance Thresholds
DEGRADATION_LOW = 10       # % - Normal maintenance
DEGRADATION_MEDIUM = 20    # % - High priority
DEGRADATION_HIGH = 30      # % - Critical

# Dust Impact Coefficients (from research)
DUST_IMPACT_FACTOR = 0.0015  # Power loss per μg/m³ of PM10
TEMP_IMPACT_FACTOR = 0.004   # Power loss per °C above optimal

# Alert Messages
ALERT_MESSAGES = {
    "cleaning": "Panel cleaning required due to dust accumulation",
    "temperature": "High temperature affecting panel performance",
    "degradation": "Performance degradation detected",
    "inspection": "Regular inspection recommended",
    "critical": "Critical performance loss - immediate action required"
}

# Maintenance Intervals (days)
CLEANING_INTERVAL_DRY_SEASON = 14
CLEANING_INTERVAL_WET_SEASON = 30
INSPECTION_INTERVAL = 90
