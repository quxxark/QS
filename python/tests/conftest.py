import pytest
import subprocess
import time
import requests
import os
from pathlib import Path
from mocks import MockBatterySensor, MockGPSSensor, MockWindSensor


@pytest.fixture(scope="session")
def controller_url():
    return "http://localhost:8080"


@pytest.fixture(scope="session")
def go_controller():
    """Start the Go controller as a subprocess"""
    # Find the Go binary
    go_path = Path(__file__).parent.parent.parent / "go" / "cmd" / "controller"
    
    # Start the controller
    process = subprocess.Popen(
        ["go", "run", "."],
        cwd=str(go_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for controller to start
    time.sleep(2)
    
    yield process
    
    # Cleanup
    process.terminate()
    process.wait()

@pytest.fixture
def sensors(controller_url):
    """Provide sensor instances"""
    return {
        "battery": MockBatterySensor(controller_url),
        "gps": MockGPSSensor(controller_url),
        "wind": MockWindSensor(controller_url),
    }

@pytest.fixture(autouse=True)
def reset_controller(controller_url):
    """Reset controller before each test"""
    time.sleep(0.1)  # Ensure previous test finished
    requests.post(f"{controller_url}/api/v1/reset")
    yield

@pytest.fixture(autouse=True)
def reset_before_each_test():
    """Автоматически сбрасывать контроллер перед каждым тестом"""
    try:
        requests.post("http://localhost:8080/api/v1/reset")
        time.sleep(0.2)  # Даём время на сброс
    except:
        pass
    yield