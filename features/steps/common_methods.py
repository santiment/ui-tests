from selenium.common.exceptions import StaleElementReferenceException

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
