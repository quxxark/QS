*** Settings ***
Documentation       Mode persistence tests
Resource            ../resources/variables.robot
Resource            ../resources/keywords.robot
Test Setup          Given controller is reset

*** Test Cases ***
Mode Persists After Trigger
    [Tags]    persistence
    When all sensors send    19.0    2.5    10.0
    Then mode should be      EMERGENCY_RETURN
    
    When all sensors send    100.0    0.5    5.0
    Then mode should be      EMERGENCY_RETURN

Order Independence - GPS First
    [Tags]    order
    When sensors send in order    G,B,W    19.0    2.5    10.0
    Then mode should be           EMERGENCY_RETURN

Order Independence - Wind First
    [Tags]    order
    When sensors send in order    W,G,B    19.0    2.5    10.0
    Then mode should be           EMERGENCY_RETURN

Order Independence - Battery First
    [Tags]    order
    When sensors send in order    B,G,W    19.0    2.5    10.0
    Then mode should be           EMERGENCY_RETURN