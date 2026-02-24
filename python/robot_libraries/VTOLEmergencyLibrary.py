"""Robot Framework library for VTOL Emergency Return testing"""
from typing import Dict, Any
import requests
import sys
from pathlib import Path

# Add path for mocks
sys.path.insert(0, str(Path(__file__).parent.parent))
from mocks import MockBatterySensor, MockGPSSensor, MockWindSensor


class VTOLEmergencyLibrary:
    """Robot Framework library for testing VTOL Emergency Return Controller"""
    
    def __init__(self):
        self.controller_url = "http://localhost:8080"
        self.battery_sensor = None
        self.gps_sensor = None
        self.wind_sensor = None
        self.last_status = None
    
    def reset_controller(self):
        """Reset controller to initial state"""
        requests.post(f"{self.controller_url}/api/v1/reset")
        self._init_sensors()
    
    def _init_sensors(self):
        """Initialize sensor mocks"""
        self.battery_sensor = MockBatterySensor(self.controller_url)
        self.gps_sensor = MockGPSSensor(self.controller_url)
        self.wind_sensor = MockWindSensor(self.controller_url)
    
    def send_sensor_data(self, battery: float, distance: float, wind: float):
        """Send data from all sensors"""
        if not self.battery_sensor:
            self._init_sensors()
        
        self.battery_sensor.send_reading(battery)
        self.gps_sensor.send_reading(distance)
        self.wind_sensor.send_reading(wind)
    
    def get_controller_mode(self) -> str:
        """Get current controller mode"""
        response = requests.get(f"{self.controller_url}/api/v1/status")
        self.last_status = response.json()
        return self.last_status["mode"]
    
    def mode_should_be(self, expected_mode: str):
        """Assert controller mode"""
        current_mode = self.get_controller_mode()
        if current_mode != expected_mode:
            raise AssertionError(f"Expected mode {expected_mode}, but got {current_mode}")
    
    def return_triggered_should_be(self, expected: bool):
        """Assert return triggered flag"""
        if not self.last_status:
            self.get_controller_mode()
        
        actual = self.last_status["return_triggered"]
        if actual != expected:
            raise AssertionError(f"Expected return_triggered={expected}, but got {actual}")
    
    def send_sensors_in_order(self, order: str, battery: float, distance: float, wind: float):
        """
        Send sensor data in specific order
        order format: "B,G,W" for Battery, GPS, Wind
        """
        if not self.battery_sensor:
            self._init_sensors()
        
        # Parse the order
        sequence = order.split(",")
        
        for sensor in sequence:
            sensor = sensor.strip().upper()
            if sensor == "B":
                self.battery_sensor.send_reading(battery)
            elif sensor == "G":
                self.gps_sensor.send_reading(distance)
            elif sensor == "W":
                self.wind_sensor.send_reading(wind)
    
    def verify_status_contains(self, key: str, expected_value: Any):
        """Verify a specific field in status"""
        if not self.last_status:
            self.get_controller_mode()
        
        actual = self.last_status.get(key)
        if actual != expected_value:
            raise AssertionError(f"Expected {key}={expected_value}, but got {actual}")