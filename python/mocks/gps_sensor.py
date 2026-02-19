"""Mock GPS sensor - sends only distance to home"""
import requests


class MockGPSSensor:
    """Simulates a GPS sensor - only knows distance to home"""
    
    def __init__(self, controller_url: str = "http://localhost:8080"):
        self.controller_url = controller_url
        self.current_distance = 0.0
    
    def send_reading(self, distance_km: float) -> None:
        """
        Send ONLY distance reading to controller.
        GPS sensor doesn't know about battery or wind.
        """
        self.current_distance = distance_km
        
        # GPS sensor only sends its own data
        payload = {
            "battery_percent": 0.0,     # GPS doesn't know this
            "distance_to_home": distance_km,
            "wind_speed": 0.0            # GPS doesn't know this
        }
        
        requests.post(
            f"{self.controller_url}/api/v1/sensor/update",
            json=payload
        )