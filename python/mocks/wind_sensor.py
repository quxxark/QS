"""Mock wind sensor - sends only wind speed"""
import requests


class MockWindSensor:
    """Simulates a wind sensor - only knows wind speed"""
    
    def __init__(self, controller_url: str = "http://localhost:8080"):
        self.controller_url = controller_url
        self.current_wind = 0.0
    
    def send_reading(self, wind_speed: float) -> None:
        """
        Send ONLY wind speed to controller.
        Wind sensor doesn't know about battery or distance.
        """
        self.current_wind = wind_speed
        
        # Wind sensor only sends its own data
        payload = {
            "battery_percent": 0.0,     # Wind sensor doesn't know this
            "distance_to_home": 0.0,    # Wind sensor doesn't know this
            "wind_speed": wind_speed
        }
        
        requests.post(
            f"{self.controller_url}/api/v1/sensor/update",
            json=payload
        )