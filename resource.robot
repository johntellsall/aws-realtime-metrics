*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           OperatingSystem
Library           Selenium2Library

*** Variables ***
${SERVER}         localhost:5000
${BROWSER}        Chrome
${DELAY}          0
${VOTING URL}      http://${SERVER}/

*** Keywords ***
Open Browser To Voting Page
    Open Browser    ${VOTING URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Reset Votes
    Voting Page Should Be Open

Voting Page Should Be Open
    Location Should Be    ${VOTING URL}
    Title Should Be    John Tells All: AWS Queue Realtime Stats

Go To Voting Page
    Go To    ${VOTING URL}
    Voting Page Should Be Open

Reset Votes
    Run    echo flushall | redis-cli 

Vote Up
    Click Element    up

Votes Not Available
    Element Text Should Be    vote-count-up    --
    Element Text Should Be    vote-count-down    --

