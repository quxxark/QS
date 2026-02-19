*** Settings ***
Documentation       Boundary conditions tests
Resource            ../resources/variables.robot
Resource            ../resources/keywords.robot
Test Setup          Given controller is reset

*** Test Cases ***
Battery Exactly 20 Percent
    [Tags]    boundary
    When all sensors send    20.0    3.0    40.0
    Then mode should be      NORMAL

Battery Slightly Below 20 Percent
    [Tags]    boundary
    When all sensors send    19.9    3.0    40.0
    Then mode should be      EMERGENCY_RETURN

Distance Exactly 2.0 km
    [Tags]    boundary
    When all sensors send    19.0    2.0    20.0
    Then mode should be      NORMAL

Distance Slightly Above 2.0 km
    [Tags]    boundary
    When all sensors send    19.0    2.1    20.0
    Then mode should be      EMERGENCY_RETURN

Wind Exactly 35 km/h
    [Tags]    boundary
    When all sensors send    19.0    1.5    35.0
    Then mode should be      NORMAL

Wind Slightly Above 35 km/h
    [Tags]    boundary
    When all sensors send    19.0    1.5    35.1
    Then mode should be      EMERGENCY_RETURN