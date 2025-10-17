"""
Common utility functions and helpers
"""
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("SPMS")

def log_info(message: str, **kwargs):
    """Log info message with optional context"""
    logger.info(message, extra=kwargs)

def log_error(message: str, **kwargs):
    """Log error message with optional context"""
    logger.error(message, extra=kwargs)

def log_warning(message: str, **kwargs):
    """Log warning message with optional context"""
    logger.warning(message, extra=kwargs)

def calculate_efficiency_loss(actual: float, predicted: float) -> float:
    """
    Calculate efficiency loss percentage
    
    Args:
        actual: Actual power output
        predicted: Predicted/expected power output
    
    Returns:
        Loss percentage (0-100)
    """
    if predicted == 0:
        return 0
    loss = ((predicted - actual) / predicted) * 100
    return max(0, min(100, loss))  # Clamp between 0-100

def get_maintenance_priority(degradation_score: float) -> str:
    """
    Determine maintenance priority based on degradation score
    
    Args:
        degradation_score: Performance degradation (0-100)
    
    Returns:
        Priority level: low, normal, high, critical
    """
    if degradation_score >= 30:
        return "critical"
    elif degradation_score >= 20:
        return "high"
    elif degradation_score >= 10:
        return "normal"
    else:
        return "low"

def format_timestamp(dt: datetime) -> str:
    """Format datetime for API responses"""
    return dt.isoformat()
