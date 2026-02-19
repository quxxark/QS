*** Settings ***
Documentation       Core emergency return logic tests
Resource            ../resources/variables.robot
Resource            ../resources/keywords.robot
Test Setup          Given controller is reset

*** Test Cases ***
Normal Conditions Should Not Trigger Return
    [Tags]    smoke    core
    When all sensors send    50.0    1.0    10.0
    Then mode should be      NORMAL

Low Battery Alone Should Not Trigger Return
    [Tags]    core
    When all sensors send    19.0    1.5    20.0
    Then mode should be      NORMAL

Low Battery With Exceeded Distance Triggers Return
    [Tags]    core    trigger
    When all sensors send    19.0    5.0    20.0
    Then mode should be      EMERGENCY_RETURN

Low Battery With Exceeded Wind Triggers Return
    [Tags]    core    trigger
    When all sensors send    19.0    1.5    40.0
    Then mode should be      EMERGENCY_RETURN

Low Battery With Both Exceeded Triggers Return
    [Tags]    core    trigger
    When all sensors send    19.0    5.0    40.0
    Then mode should be      EMERGENCY_RETURN

Normal Battery With Exceeded Conditions Does Not Trigger Return
    [Tags]    core    negative
    When all sensors send    21.0    5.0    40.0
    Then mode should be      NORMAL