*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
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
    Voting Page Should Be Open

Voting Page Should Be Open
    Title Should Be    John Tells All: AWS Queue Realtime Stats

Go To Voting Page
    Go To    ${VOTING URL}
    Voting Page Should Be Open

# Input Username
#     [Arguments]    ${username}
#     Input Text    username_field    ${username}

# Input Password
#     [Arguments]    ${password}
#     Input Text    password_field    ${password}

# Submit Credentials
#     Click Button    Voting_button

# Welcome Page Should Be Open
#     Location Should Be    ${WELCOME URL}
#     Title Should Be    Welcome Page
