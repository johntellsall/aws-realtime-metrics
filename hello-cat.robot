*** Settings ***
Resource          resource.robot
Test Setup        Reset Votes
Suite Setup       Open Browser To Voting Page
Suite Teardown    Close All Browsers

*** Test Cases ***
Valid Page
    Votes Not Available

Register Up Vote
    Vote Up
    Element Text Should Be    vote-count-up    1
    Element Text Should Be    vote-count-down    0

Register Down Vote
    Vote Down
    Element Text Should Be    vote-count-up    0
    Element Text Should Be    vote-count-down    1

Register Multiple
    Vote Up
    Vote Down
    Vote Up
    Element Text Should Be    vote-count-up    2
    Element Text Should Be    vote-count-down    1

