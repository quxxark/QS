*** Settings ***
Documentation       Common variables for VTOL emergency tests

*** Variables ***
${CONTROLLER_URL}      http://localhost:8080
${MODE_NORMAL}         NORMAL
${MODE_EMERGENCY}      EMERGENCY_RETURN

# Thresholds
${CRITICAL_BATTERY}    20.0
${MAX_DISTANCE}        2.0
${MAX_WIND}            35.0