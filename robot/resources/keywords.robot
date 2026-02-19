*** Settings ***
Documentation       Common keywords for VTOL emergency tests
Library             ../../python/robot_libraries/VTOLEmergencyLibrary.py

*** Keywords ***
Given controller is reset
    Reset controller

When all sensors send
    [Arguments]    ${battery}    ${distance}    ${wind}
    Send sensor data    ${battery}    ${distance}    ${wind}

Then mode should be
    [Arguments]    ${expected_mode}
    Mode should be    ${expected_mode}

And return triggered flag should be
    [Arguments]    ${expected}
    Return triggered should be    ${expected}

When sensors send in order
    [Arguments]    ${order}    ${battery}    ${distance}    ${wind}
    Send sensors in order    ${order}    ${battery}    ${distance}    ${wind}