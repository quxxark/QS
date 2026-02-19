# VTOL Flight Control Test Challenge

Tests implementation for a critical VTOL flight scenario  

## Features

- VTOL FW simulation based on GO-lang (for demo-purposes)  
- Feature tests implementation on pytest lib (separated)  
- Feature tests implementation on RobotFW lib (separated)  
- Sensors mocking  
- CI/CD ready (.github/workwlows/test.yml)  

## Quick Start

- OS Ubuntu / MacOS  
- Python 3.13  
- GoLang 1.21  
- pip3  

## Requirements

- Critical battery level: <20%  
- An emergency landing executution when Battery has a critical level AND (distance > 2 km OR wind speed > 35 km/h)  

## Local Development Workflow

- Build the demo FCS: `go build go/cmd/controller/main.go -o ../../../bin/controller`  
- Run build binary: `./bin/controller &`  
- `cd python`  
- Create Virtual Environment:`python3 -m venv venv`  
- Activate Virtual Environment: `source venv/bin/activate`  
- Install Test Dependencies: `pip3 install -r requirements.txt`  
- Run Tests with Robot FW: `python3 -m robot --outputdir output --variable CONTROLLER_URL:http://localhost:8080 --timestampoutputs test_suites/`  
- Run Tests with pytest: `python3 -m pytest tests/ -v --tb=short --no-header`  
- Deactivate Virtual Environment: `deactivate`  
- Test Results:  
  -- Pytest: `./python/tests/reports/`  
  -- Robot FW: `./robot/output/`  

## Alternative tests execution (one-button-solution)
- Run Pytest Tests: `./run_pytest_tests.sh`  
- Run Robot FW Tests: `./run_robot_tests.sh`  

## Project structure

QUANTUM-SYSTEMS/  
├── .github  
|   └── workflows  
|       └── test.yml            # GitHub Actions configuration (CI/CD)  
├── bin                         # Build FCS binary (for DEMO purposes)  
├── go                          # Source code for FCS binary (for DEMO purposes)  
|   └── ...  
├── python  
│   ├── mocks/                  # Sensors mocks  
│   ├── robot_libraries/        # Robot FW steps implementation  
│   ├── tests/                  # pytest lib tests implementation  
│   |   ├── reports/            # pytest tests execution reports  
│   |   ├── conftest.py         # pytest fixtures  
│   |   └── test_emergency.py   # pytest tests  
│   └── requirements.txt        # testing dependencies  
├── robot  
│   ├── output/                 # Robot FW tests execution reports  
│   ├── resources/              # Robot FW common keywords implementation  
│   ├── test-suits/             # Robot FW test cases implementation  
├── run_pytest_tests.sh         # Prepared script for pytest-tests execuition (on-button-solution)  
├── run_robot_tests.sh          # Prepared script for RobotFW-tests execuition (on-button-solution)  
├── TestPlan.pdf                # Feature testing Test plan  
└── HIL-SIL-spec.pdf            # HIl/SIL documentation  

## GitHub Actions Workflow

The project includes automated testing via GitHub Actions
Trigger: On pull requests to main or develop branches

## Branch Protection Rules

- Status checks must pass before merging
- Branches must be up to date
- Required: Regression tests passing

