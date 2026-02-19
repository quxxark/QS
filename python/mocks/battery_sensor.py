"""Mock battery sensor - sends only battery level to controller"""
import requests
from typing import Optional


class MockBatterySensor:
    """Simulates a battery sensor - only knows battery level"""
    
    def __init__(self, controller_url: str = "http://localhost:8080"):
        self.controller_url = controller_url
        self.current_level = 100.0
    
    def send_reading(self, level: Optional[float] = None) -> None:
        """
        Send ONLY battery reading to controller.
        Battery sensor doesn't know about distance or wind.
        """
        if level is not None:
            self.current_level = level
        
        # Battery sensor only sends its own data
        # Other sensors will send their own data separately
        payload = {
            "battery_percent": self.current_level,
            "distance_to_home": 0.0,  # Battery doesn't know this
            "wind_speed": 0.0          # Battery doesn't know this
        }
        
        requests.post(
            f"{self.controller_url}/api/v1/sensor/update",
            json=payload
        )