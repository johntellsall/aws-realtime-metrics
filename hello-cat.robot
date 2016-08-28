*** Settings ***
Documentation     A test suite with a single test for valid login.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Test Cases ***
Valid Page
    Open Browser To Voting Page
    Votes Not Available
    [Teardown]    Close Browser

Register Up Vote
    Open Browser To Voting Page
    Vote Up
    Element Text Should Be    vote-count-up    1
    Element Text Should Be    vote-count-down    0
    [Teardown]    Close Browser
