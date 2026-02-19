#!/bin/bash
set -e

# VTOL Emergency Return System - Test Runner
# Minimal output for CI/CD pipelines

# Build Go controller
cd go/cmd/controller
go mod download
go build -o ../../../bin/controller
cd ../../..

# Start controller in background
./bin/controller &
CONTROLLER_PID=$!

# Setup Python virtual environment
cd python
[ -d "venv" ] || python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

# Wait for controller to initialize
sleep 3

# Verify controller is running
if ! kill -0 $CONTROLLER_PID 2>/dev/null; then
    echo "[ ERROR ] Controller failed to start"
    exit 1
fi

# Run tests
set +e
python -m pytest tests/ -v --tb=short --no-header
TEST_RESULT=$?
set -e

# Stop controller
kill $CONTROLLER_PID 2>/dev/null || true
wait $CONTROLLER_PID 2>/dev/null || true

# Deactivate virtual environment
deactivate 2>/dev/null || true
cd ..

# Print final result
if [ $TEST_RESULT -eq 0 ]; then
    echo "[ INFO ] All tests passed"
else
    echo "[ ERROR ] Tests failed (exit code: $TEST_RESULT)"
fi

exit $TEST_RESULT