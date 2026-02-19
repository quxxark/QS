#!/bin/bash
set -e

# VTOL Robot Framework Test Runner

cleanup_port() {
    if command -v lsof &> /dev/null; then
        PIDS=$(lsof -ti:8080 2>/dev/null || true)
    elif command -v netstat &> /dev/null; then
        PIDS=$(netstat -tulpn 2>/dev/null | grep :8080 | awk '{print $7}' | cut -d'/' -f1 || true)
    else
        PIDS=$(pgrep -f "bin/controller" 2>/dev/null || true)
    fi
    
    if [ -n "$PIDS" ]; then
        kill -9 $PIDS 2>/dev/null || true
        sleep 1
    fi
}

cleanup() {
    if [ -n "$CONTROLLER_PID" ] && kill -0 $CONTROLLER_PID 2>/dev/null; then
        kill $CONTROLLER_PID 2>/dev/null || true
        wait $CONTROLLER_PID 2>/dev/null || true
    fi
    cleanup_port
    deactivate 2>/dev/null || true
}

trap cleanup EXIT INT TERM

# Clean port before starting
cleanup_port

# Build Go controller
cd go/cmd/controller
go build -o ../../../bin/controller
cd ../../..

# Start controller
./bin/controller &
CONTROLLER_PID=$!

# Wait for controller to be ready
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8080/api/v1/status > /dev/null 2>&1; then
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 1
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "[ ERROR ] Controller failed to start"
    exit 1
fi

# Setup Python environment
cd python
[ -d "venv" ] || python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install requests robotframework robotframework-requests > /dev/null 2>&1

# Run Robot tests
cd ../robot
mkdir -p output
rm -rf output/* 2>/dev/null || true

python -m robot --outputdir output \
                --variable CONTROLLER_URL:http://localhost:8080 \
                --timestampoutputs \
                test_suites/

ROBOT_RESULT=$?

# Print only essential results
echo ""
if [ $ROBOT_RESULT -eq 0 ]; then
    echo "[ INFO ] All tests passed"
else
    echo "[ ERROR ] Tests failed (exit code: $ROBOT_RESULT)"
fi
echo "[ INFO ] Report: $(pwd)/output/report.html"

exit $ROBOT_RESULT