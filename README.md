# ui-tests
This project contains automated tests for Sanbase UI

## Installation
There're 2 ways to run tests: on your machine - with your browser or with Browserstack, or from a Docker container (only using Browserstack)
If you want to run tests on your machine, first do:
```
pip install -r requirements.txt
```

## Configuration
constants.py contain the list of environmental variables, available to configure the test run:
```
CONFIG_FILE - path to json file containing browser configuration
WHERE_TO_RUN - locally or using Browserstack
TASK_ID, BROWSERSTACK_USERNAME, BROWSERSTACK_SERVER, BROWSERSTACK_ACCESS_KEY, BROWSERSTACK_APP_ID - Browserstack configurations, more on that here: https://www.browserstack.com/automate/behave
ENVIRONMENT - 'stage' or 'prod'
BOT_LOGIN_SECRET_ENDPOINT - url for Sanbase enpdoint which sets up bot login cookie
BOT_USER_ID - # of bot user (multiple bots are used for parallel testing)
DISCORD_WEBHOOK, DISCORD_USER_ID - Discord configurations for posting test results
```

## Running the tests

Tests are based on Behave framework (https://behave.readthedocs.io/en/latest/)

To run tests, first go to `features` directory:
```
cd features
```
Here's an example of how to run the tests:
```
behave mainpage.feature --tags=stage
```
This command will run all test scenarios contained in `mainpage.feature` which are marked by `stage` tag. More info on tags and run options you can find under the link above.