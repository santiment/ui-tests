from seleniumwire import webdriver
from browserstack.local import Local
import os, json
from constants import WHERE_TO_RUN, CONFIG_FILE, TASK_ID, BROWSERSTACK_SERVER, BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, BROWSERSTACK_APP_ID

CONFIG_FILE_PATH = os.path.join('..', 'config', '{0}.json'.format(CONFIG_FILE))

with open(CONFIG_FILE_PATH) as data_file:
    CONFIG = json.load(data_file)

bs_local = None

def start_local():
    """Code to start browserstack local before start of test."""
    global bs_local
    bs_local = Local()
    bs_local_args = { "key": BROWSERSTACK_ACCESS_KEY, "forcelocal": "true" }
    bs_local.start(**bs_local_args)

def stop_local():
    """Code to stop browserstack local after end of test."""
    global bs_local
    if bs_local is not None:
        bs_local.stop()


def before_feature(context, feature):
    if WHERE_TO_RUN == 'local':
        chromedriver_path = os.path.realpath(os.path.join(os.getcwd(), '..', 'bin', 'chromedriver'))
        if chromedriver_path not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + chromedriver_path
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        context.browser = webdriver.Chrome(chrome_options=options)
    else:
        desired_capabilities = CONFIG['environments'][TASK_ID]

        for key in CONFIG["capabilities"]:
            if key not in desired_capabilities:
                desired_capabilities[key] = CONFIG["capabilities"][key]

        if BROWSERSTACK_APP_ID:
            desired_capabilities['app'] = BROWSERSTACK_APP_ID

        if "browserstack.local" in desired_capabilities and desired_capabilities["browserstack.local"]:
            start_local()

        context.browser = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor="http://%s:%s@%s/wd/hub" % (BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, BROWSERSTACK_SERVER)
        )

def after_feature(context, feature):
    context.browser.quit()
    stop_local()
