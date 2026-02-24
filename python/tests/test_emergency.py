"""
VTOL Emergency Return Controller

Focus:
- Minimal but complete safety coverage
- Boundary conditions included in parametrization
- No redundant test duplication
"""

import pytest
import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from mocks import MockBatterySensor, MockGPSSensor, MockWindSensor


BASE_URL = "http://localhost:8080"
MODE_NORMAL = "NORMAL"
MODE_EMERGENCY = "EMERGENCY_RETURN"


def send_sensor_data(sensors, battery, distance, wind):
    """Simulate independent sensor updates"""
    sensors["battery"].send_reading(battery)
    sensors["gps"].send_reading(distance)
    sensors["wind"].send_reading(wind)


def get_status(controller_url):
    response = requests.get(f"{controller_url}/api/v1/status")
    assert response.status_code == 200
    return response.json()


@pytest.mark.parametrize(
    "battery,distance,wind,expected_mode",
    [
        # Normal conditions
        (50.0, 1.0, 10.0, MODE_NORMAL),
        (19.0, 1.5, 20.0, MODE_NORMAL),

        # Distance triggers
        (19.0, 5.0, 20.0, MODE_EMERGENCY),

        # Wind triggers
        (19.0, 1.5, 40.0, MODE_EMERGENCY),

        # Wind + distance
        (19.0, 5.0, 40.0, MODE_EMERGENCY),

        # Battery is in normale state
        (21.0, 5.0, 40.0, MODE_NORMAL),
    ],
)
def test_emergency_return_logic(controller_url, sensors, battery, distance, wind, expected_mode):
    """
    Validate core emergency return decision matrix.
    Covers:
    - Normal behavior
    - Distance trigger
    - Wind trigger
    - Both triggers
    - Battery above threshold
    """

    send_sensor_data(sensors, battery, distance, wind)
    status = get_status(controller_url)
    assert status["mode"] == expected_mode


@pytest.mark.parametrize(
    "battery,distance,wind,expected_mode",
    [
        # Battery boundary
        (20.0, 3.0, 40.0, MODE_NORMAL),
        (19.9, 3.0, 40.0, MODE_EMERGENCY),

        # Distance boundary
        (19.0, 2.0, 20.0, MODE_NORMAL),
        (19.0, 2.1, 20.0, MODE_EMERGENCY),

        # Wind boundary
        (19.0, 1.5, 35.0, MODE_NORMAL),
        (19.0, 1.5, 35.1, MODE_EMERGENCY),
    ],
)
def test_boundary_conditions(
    controller_url, sensors, battery, distance, wind, expected_mode
):
    """
    Validate strict comparison logic:
    - Battery < 20%
    - Distance > 2 km
    - Wind > 35 km/h
    """

    send_sensor_data(sensors, battery, distance, wind)
    status = get_status(controller_url)

    assert status["mode"] == expected_mode

def test_mode_persistence_after_trigger(controller_url, sensors):
    """
    Once EMERGENCY_RETURN is activated,
    controller must not revert back to NORMAL.
    """

    # Trigger emergency
    send_sensor_data(sensors, 19.0, 2.5, 10.0)
    status = get_status(controller_url)
    assert status["mode"] == MODE_EMERGENCY

    # Send safe conditions
    send_sensor_data(sensors, 100.0, 0.5, 5.0)
    status = get_status(controller_url)

    assert status["mode"] == MODE_EMERGENCY

def test_sensor_update_order_independence(controller_url):
    """
    Emergency decision must be independent
    of sensor update order.
    """

    battery = MockBatterySensor(controller_url)
    gps = MockGPSSensor(controller_url)
    wind = MockWindSensor(controller_url)

    # Order variation
    gps.send_reading(2.5)
    wind.send_reading(10.0)
    battery.send_reading(19.0)

    status = get_status(controller_url)
    assert status["mode"] == MODE_EMERGENCY