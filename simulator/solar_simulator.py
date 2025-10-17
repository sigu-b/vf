"""
Main Solar Panel IoT Simulator
Sends realistic sensor data to the backend API
"""
import requests
import time
import json
from datetime import datetime
from simulator.config import (
    API_BASE_URL,
    SENSOR_UPLOAD_ENDPOINT,
    SIMULATION_INTERVAL,
    PANELS
)
from simulator.weather_patterns import WeatherSimulator
from simulator.physics_model import calculate_power_output
from simulator.data_logger import DataLogger

class SolarPanelSimulator:
    """
    Simulates multiple solar panels with realistic IoT sensor data
    """
    
    def __init__(self, panel_ids=None):
        self.panel_ids = panel_ids or PANELS
        self.weather_sim = WeatherSimulator()
        self.data_logger = DataLogger()
        self.api_url = f"{API_BASE_URL}{SENSOR_UPLOAD_ENDPOINT}"
        self.iteration = 0
        
    def generate_sensor_reading(self, panel_id):
        """
        Generate sensor reading for a specific panel
        """
        # Get environmental conditions
        conditions = self.weather_sim.get_current_conditions()
        
        # Add per-panel variation (microclimate, orientation, etc.)
        panel_variation = hash(panel_id) % 10 / 100.0  # 0-10% variation
        
        irradiance = conditions['irradiance'] * (1 + panel_variation)
        temperature = conditions['temperature'] + (panel_variation * 5)
        
        # Calculate power output using physics model
        power_output = calculate_power_output(
            irradiance=irradiance,
            temperature=temperature,
            pm10=conditions['pm10'],
            pm25=conditions['pm25'],
            humidity=conditions['humidity']
        )
        
        # Create sensor reading payload
        reading = {
            'panel_id': panel_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'pm10': round(conditions['pm10'], 2),
            'pm25': round(conditions['pm25'], 2),
            'temperature': round(temperature, 2),
            'humidity': round(conditions['humidity'], 2),
            'irradiance': round(irradiance, 2),
            'power_output': round(power_output, 2)
        }
        
        return reading
    
    def send_to_api(self, reading):
        """
        Send sensor reading to backend API
        """
        try:
            response = requests.post(
                self.api_url,
                json=reading,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 201:
                print(f"✓ {reading['panel_id']}: {reading['power_output']}W "
                      f"(Irr: {reading['irradiance']}W/m², PM10: {reading['pm10']}μg/m³)")
                return True
            else:
                print(f"✗ API Error {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"✗ Connection failed. Is the backend running at {API_BASE_URL}?")
            return False
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return False
    
    def run_single_iteration(self):
        """
        Run one iteration: generate and send data for all panels
        """
        self.iteration += 1
        print(f"\n[Iteration {self.iteration}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for panel_id in self.panel_ids:
            reading = self.generate_sensor_reading(panel_id)
            
            # Send to API
            success = self.send_to_api(reading)
            
            # Log to CSV
            if success:
                self.data_logger.log_reading(reading)
    
    def run_continuous(self, interval=None):
        """
        Run simulator continuously
        """
        interval = interval or SIMULATION_INTERVAL
        
        print("=" * 70)
        print("Solar Panel IoT Simulator Started")
        print("=" * 70)
        print(f"API Endpoint: {self.api_url}")
        print(f"Panels: {', '.join(self.panel_ids)}")
        print(f"Interval: {interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.run_single_iteration()
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nSimulator stopped by user")
            print(f"Total iterations: {self.iteration}")
            self.data_logger.close()

def main():
    """
    Main entry point for simulator
    """
    simulator = SolarPanelSimulator()
    simulator.run_continuous()

if __name__ == "__main__":
    main()
