import os


BOT_LOGIN_SECRET_ENDPOINT = os.environ['BOT_LOGIN_SECRET_ENDPOINT']
CONFIG_FILE = os.getenv('CONFIG_FILE', 'single')
TASK_ID = int(os.getenv('TASK_ID', 0))
BROWSERSTACK_USERNAME = os.environ['BROWSERSTACK_USERNAME']
BROWSERSTACK_SERVER = os.getenv('BROWSERSTACK_SERVER', 'hub.browserstack.com')
BROWSERSTACK_ACCESS_KEY = os.environ['BROWSERSTACK_ACCESS_KEY']
BROWSERSTACK_APP_ID = os.getenv('BROWSERSTACK_APP_ID', None)
WHERE_TO_RUN = os.getenv('WHERE_TO_RUN', 'bs')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'stage')
