"""
Data logger for simulator - saves readings to CSV
"""
import csv
import os
from datetime import datetime

class DataLogger:
    """
    Logs simulated sensor data to CSV files
    """
    
    def __init__(self, log_dir='simulator/logs'):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(log_dir, f'simulation_{timestamp}.csv')
        
        # Initialize CSV file
        self.fieldnames = [
            'timestamp', 'panel_id', 'pm10', 'pm25',
            'temperature', 'humidity', 'irradiance', 'power_output'
        ]
        
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
        
        print(f"Logging to: {self.log_file}\n")
    
    def log_reading(self, reading):
        """
        Append sensor reading to CSV log
        """
        try:
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writerow(reading)
        except Exception as e:
            print(f"Logging error: {e}")
    
    def close(self):
        """
        Close logger and print summary
        """
        print(f"\nLog saved to: {self.log_file}")
