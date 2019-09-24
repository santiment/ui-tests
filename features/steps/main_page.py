from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datastorage import metrics, selectors, xpaths, chart_settings_options, delta, bot_url, title_conversion, urls
from selenium.webdriver.common.action_chains import ActionChains
from constants import BOT_LOGIN_SECRET_ENDPOINT, ENVIRONMENT

class MaxAttemptsLimitException(Exception):
    pass

class MissingCategoryException(Exception):
    pass

class MissingMetricException(Exception):
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

class Mainpage:

    def __init__(self, driver, is_logged_in):
        self.default_url = urls[ENVIRONMENT]
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)
        if is_logged_in:
            url = bot_url + BOT_LOGIN_SECRET_ENDPOINT
            self.driver.get(url)

    def navigate_to_main_page(self):
        attempts = 0
        selector = selectors["token_image"]
        while attempts < 5:
            try:
                self.driver.get(self.default_url)
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                return
            except TimeoutException:
                attempts += 1
        raise MaxAttemptsLimitException("Exceeded max attempts limit trying to load main page")

    def close_cookie_popup(self):
        xpath = xpaths["close_cookies_button"]
        logging.info("Trying to close cookie popup")
        try:
            button = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            safe_click(button)
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logging.info("Already closed")
        logging.info("Closed successfully")

    def close_explore_popup(self):
        xpath = xpaths["close_assets_button"]
        logging.info("Trying to close explore assets popup")
        try:
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            safe_click(button)
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logging.info("Already closed")
        logging.info("Closed successfully")

    def get_chart_page_element(self):
        xpath = xpaths["chart_page_element"]
        return self.driver.find_element_by_xpath(xpath)

    def get_search_dialog(self):
        selector = selectors["search_dialog"]
        return self.driver.find_element_by_css_selector(selector)

    def get_search_input_element(self):
        selector = selectors["search_input"]
        return self.get_search_dialog().find_element_by_css_selector(selector)

    def get_search_result_element(self, text):
        logging.info("Getting search result for '{0}'".format(text))
        xpath = xpaths["search_result"]
        search_result_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        for element in search_result_elements:
            if text.lower() in element.text.lower():
                    return element
        raise ValueError("No search result found for '{0}'".format(text))

    def search(self, text):
        logging.info("Searching for '{0}'".format(text))
        self.open_search_dialog()
        search_input_element = self.get_search_input_element()
        search_input_element.send_keys(text)

    def search_and_select(self, text):
        self.search(text)
        safe_click(self.get_search_result_element(text))
        selector_dialog = selectors["search_dialog"]
        selector_image = selectors['token_image']
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector_dialog)))
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector_image)))

    def get_period_selector_element(self, period):
        logging.info("Getting period selector for {0}".format(period))
        xpath = xpaths["period_selector"].format(period)
        return self.get_chart_page_element().find_element_by_xpath(xpath)

    def select_period(self, period):
        logging.info("Selecting period {0}".format(period))
        xpath = xpaths["period_selector_active"]
        safe_click(self.get_period_selector_element(period))
        self.wait.until(
            lambda wd: wd.find_element_by_xpath(xpath).text == period
        )
        selector = selectors["chart_loader"]
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_metrics_menu_element(self):
        selector = selectors["metrics_menu"]
        return self.driver.find_element_by_css_selector(selector)

    def get_metrics_categories_element(self):
        selector = selectors["metrics_categories"]
        logging.info("Waiting until category list loads")
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_metrics_category_elements(self):
        xpath = xpaths["metrics_category"]
        return self.get_metrics_menu_element().find_elements_by_xpath(xpath)

    def get_metrics_category_element(self, category):
        logging.info("Getting metrics category element {0}".format(category))
        for element in self.get_metrics_category_elements():
            if category in element.text:
                return element
        raise MissingCategoryException("Category {0} not found for the selected token".format(category))

    def select_metrics_category(self, category):
        logging.info("Selecting metrics category {0}".format(category))
        xpath = xpaths["metrics_category_active"].format(category)
        safe_click(self.get_metrics_category_element(category))
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def get_metrics_list_element(self):
        selector = selectors["metrics_list"]
        logging.info("Waiting until metrics list loads")
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_metric_elements(self):
        xpath = xpaths["metric"]
        return self.get_metrics_list_element().find_elements_by_xpath(xpath)

    def get_metric_element(self, metric):
        logging.info("Getting metric element {0}".format(metric))
        for element in self.get_metric_elements():
            if element.text == metric:
                return element
        raise MissingMetricException("Metric {0} not found for the selected token".format(metric))

    def get_active_metrics_panel_element(self):
        selector = selectors["active_metrics_panel"]
        return self.get_chart_page_element().find_element_by_css_selector(selector)

    def get_active_metric_element(self, metric):
        logging.info("Getting active metric element {0}".format(metric))
        xpath = xpaths["active_metric"].format(metric)
        return self.get_active_metrics_panel_element().find_element_by_xpath(xpath)

    def get_all_active_metric_elements(self):
        xpath = xpaths["any_active_metric"]
        return self.get_active_metrics_panel_element().find_elements_by_xpath(xpath)

    def get_all_active_metrics(self):
        return [x.text for x in self.get_all_active_metric_elements()]

    def get_close_active_metric_element(self, active_metric):
        selector = selectors["close_active_metric"]
        return active_metric.find_element_by_css_selector(selector)

    def select_metric(self, metric):
        try:
            self.get_active_metric_element(metric)
        except NoSuchElementException:
            self.open_metrics_menu()
            xpath = xpaths["active_metric"].format(metric)
            self.select_metrics_category(metrics[metric][0])
            metric_element = self.get_metric_element(metric)
            safe_click(metric_element)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            self.close_metrics_menu()


    def deselect_metric(self, metric):
        logging.info("Trying to deselect {0} metric".format(metric))
        try:
            active_metric = self.get_active_metric_element(metric)
            safe_click(self.get_close_active_metric_element(active_metric))
            self.wait.until(EC.invisibility_of_element(active_metric))
        except NoSuchElementException:
            pass

    def clear_all_active_metrics(self):
        active_metrics = self.get_all_active_metrics()
        logging.info("{0} active metrics to remove".format(len(active_metrics)))
        for metric in active_metrics:
            self.deselect_metric(metric)
        active_metrics = self.get_all_active_metrics()
        logging.info("{0} metrics left after removal".format(len(active_metrics)))

    def get_share_dialog(self):
        selector = selectors["share_dialog"]
        return self.driver.find_element_by_css_selector(selector)

    def get_share_link_element(self):
        selector = selectors["share_link"]
        return self.get_share_dialog().find_element_by_css_selector(selector)

    def get_share_link_value(self):
        return self.get_share_link_element().get_attribute('value')

    def get_chart_header_element(self):
        selector = selectors["chart_header_element"]
        return self.driver.find_element_by_css_selector(selector)

    def get_token_selector_element(self):
        selector = selectors["token_selector_element"]
        return self.driver.find_element_by_css_selector(selector)

    def open_share_dialog(self):
        logging.info("Opening share dialog")
        selector = selectors["share_dialog"]
        try:
            logging.info("Checking if share dialog is open")
            self.get_share_dialog()
            logging.info("Share dialog is open, doing nothing")
        except NoSuchElementException:
            logging.info("Share dialog is not open, clicking the button")
            self.open_chart_settings_menu()
            safe_click(self.get_chart_settings_menu_item("share"))
            logging.info("Waiting until share dialog is open")
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def close_share_dialog(self):
        selector = selectors["close_share_dialog"]
        logging.info("Closing share dialog")
        try:
            dialog = self.get_share_dialog()
            close_button = dialog.find_element_by_css_selector(selector)
            safe_click(close_button)
            self.wait.until(EC.invisibility_of_element(dialog))
            logging.info("Closed share dialog")
            self.close_chart_settings_menu()
        except NoSuchElementException:
            logging.info("Already closed")
            self.close_chart_settings_menu()

    def open_search_dialog(self):
        selector = selectors["search_dialog"]
        try:
            logging.info("Checking if search dialog is open")
            self.get_share_dialog()
            logging.info("Search dialog is open, doing nothing")
        except NoSuchElementException:
            logging.info("Search dialog is not open, clicking the button")
            safe_click(self.get_token_selector_element())
            logging.info("Waiting until search dialog is open")
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def close_search_dialog(self):
        selector = selectors["close_search_dialog"]
        try:
            dialog = self.get_search_dialog()
            close_button = dialog.find_element_by_css_selector(selector)
            safe_click(close_button)
            self.wait.until(EC.invisibility_of_element(dialog))
        except NoSuchElementException:
            pass

    def get_metrics_menu_button(self):
        selector = selectors["metrics_menu_button"]
        return self.get_chart_page_element().find_element_by_css_selector(selector)

    def get_modal_overlay(self):
        selector = selectors["modal_overlay"]
        return self.driver.find_element_by_css_selector(selector)

    def open_metrics_menu(self):
        logging.info("Opening metrics menu")
        xpath = xpaths["metric"]
        try:
            self.get_metrics_menu_element()
            logging.info("Already opened")
        except NoSuchElementException:
            safe_click(self.get_metrics_menu_button())
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            logging.info("Menu opened")

    def close_metrics_menu(self):
        logging.info("Closing metrics menu")
        selector = selectors["metrics_menu_title"]
        try:
            safe_click(self.get_modal_overlay())
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info("Menu closed")
        except NoSuchElementException:
            logging.info("Already closed")

    def get_chart_settings_button(self):
        selector = selectors["chart_settings_button"]
        return self.get_chart_page_element().find_element_by_css_selector(selector)

    def get_chart_settings_menu_element(self):
        selector = selectors["chart_settings_menu"]
        return self.driver.find_element_by_css_selector(selector)

    def open_chart_settings_menu(self):
        logging.info("Opening chart settings menu")
        selector = selectors["chart_settings_menu"]
        try:
            self.get_chart_settings_menu_element()
            logging.info("Already opened")
        except NoSuchElementException:
            safe_click(self.get_chart_settings_button())
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info("Menu opened")

    def close_chart_settings_menu(self):
        logging.info("Closing chart settings menu")
        selector = selectors["chart_settings_menu"]
        try:
            safe_click(self.get_modal_overlay())
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info("Menu closed")
        except NoSuchElementException:
            logging.info("Already closed")

    def get_chart_settings_menu_item(self, option):
        xpath = xpaths["chart_settings_menu_item"].format(chart_settings_options[option])
        return self.get_chart_settings_menu_element().find_element_by_xpath(xpath)

    def get_token_title_element(self):
        selector = selectors["token_title"]
        return self.driver.find_element_by_css_selector(selector)

    def get_token_title(self):
        return self.get_token_title_element().text

    def get_from_to_dates(self):
        selector = selectors["calendar_dates"]
        [date_from_text, date_to_text] = self.get_chart_page_element().find_element_by_css_selector(selector).text.split('-')
        datetime_from = datetime.strptime(date_from_text.strip(), '%d.%m.%y')
        datetime_to = datetime.strptime(date_to_text.strip(), '%d.%m.%y')
        return datetime_from, datetime_to

    def get_interval(self):
        selector = selectors["interval"]
        return self.get_chart_page_element().find_element_by_css_selector(selector).text

    def get_chart_date(self, order):
        selector = selectors["chart_date"]
        if order not in ("first", "last"):
            raise ValueError("Unsupported order: {0}".format(order))
        return self.get_chart_page_element().find_element_by_css_selector(selector.format(order)).text

    def get_token_image_element(self):
        selector = selectors["token_image"]
        return self.get_chart_header_element().find_element_by_css_selector(selector)

    def get_token_description_element(self):
        selector = selectors["token_description"]
        return self.get_chart_header_element().find_element_by_css_selector(selector)

    def get_token_price_element(self):
        selector = selectors["token_price"]
        return self.get_chart_header_element().find_element_by_css_selector(selector)

    def get_token_volume_element(self):
        selector = selectors["token_volume"]
        return self.get_chart_header_element().find_element_by_css_selector(selector)

    def get_token_currency_element(self):
        selector = selectors["token_volume_currency"]
        return self.get_chart_header_element().find_element_by_css_selector(selector)

    def get_add_signal_button(self):
        selector = selectors["add_signal_button"]
        return self.get_chart_header_element().find_element_by_css_selector(selector)

    def get_watch_button(self):
        selector = selectors["watch_button"]
        return self.get_chart_header_element().find_element_by_css_selector(selector)

    def get_account_menu_button(self):
        selector = selectors["account_menu_button"]
        return self.driver.find_element_by_css_selector(selector)

    def open_account_menu(self):
        button = self.get_account_menu_button()
        safe_click(button)
        selector = selectors["account_menu"]
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_active_period_element(self):
        xpath = xpaths["period_selector_active"]
        return self.driver.find_element_by_xpath(xpath)
