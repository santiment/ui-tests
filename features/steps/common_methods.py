from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
import time
from constants import ENVIRONMENT, BOT_LOGIN_SECRET_ENDPOINT, BOT_USER_ID
from datastorage import urls

class MaxAttemptsLimitException(Exception):
    pass

class ClickError(Exception):
    pass

def safe_click(element):
    attempts = 0
    while attempts < 10:
        try:
            element.click()
            return
        except StaleElementReferenceException:
            time.sleep(0.5)
            attempts += 1
    raise ClickError("Exceeded max click attempts limit on element {0}".format(element))

def set_login_cookie(driver):
    url = urls[ENVIRONMENT]['bot'] + BOT_LOGIN_SECRET_ENDPOINT
    if BOT_USER_ID:
        url = f'{url}/{BOT_USER_ID}'
    driver.get(url)