from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selectors_main import *
from datastorage import metrics, chart_settings_options, delta, title_conversion, urls
from constants import BOT_LOGIN_SECRET_ENDPOINT, ENVIRONMENT, CONFIG_FILE, BOT_USER_ID
from common_methods import ClickError, MaxAttemptsLimitException, safe_click, set_login_cookie
from localstorage import LocalStorage

class MissingCategoryException(Exception):
    pass

class MissingMetricException(Exception):
    pass

class Mainpage:

    def __init__(self, driver, is_logged_in):
        self.default_url = urls[ENVIRONMENT]['main']
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60, ignored_exceptions=[StaleElementReferenceException])
        if is_logged_in:
            set_login_cookie(self.driver)

    def basic_wait(self, selector, flag, timeout=None):
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        if flag:
            wait.until(
                lambda wd: self.driver.find_element_by_css_selector(selector).is_displayed()
            )
        else:
            wait.until_not(
                lambda wd: self.driver.find_element_by_css_selector(selector).is_displayed()
            )

    def find_element_anti_stale(self, selector):
        attempts = 0
        while attempts < 5:
            try:
                element = self.driver.find_element_by_css_selector(selector)
                time.sleep(1)
                element.is_displayed()
            except StaleElementReferenceException:
                attempts += 1
            else:
                return element
        raise StaleElementReferenceException(f"Exceeded max attempts limit trying to get element {selector}")

    def find_elements_anti_stale(self, selector):
        attempts = 0
        while attempts < 5:
            try:
                elements = self.driver.find_elements_by_css_selector(selector)
                time.sleep(1)
                [element.is_displayed() for element in elements]
            except StaleElementReferenceException:
                attempts += 1
            else:
                return elements
        raise StaleElementReferenceException(f"Exceeded max attempts limit trying to get element {selector}")

    def hide_popups(self):
        storage = LocalStorage(self.driver)
        storage.set("LS_SIDECAR_TOOLTIP_SHOWN_TRIGGER_FORM_EXPLANATION", 1)
        storage.set("LS_SIDECAR_TOOLTIP_SHOWN_SOCIAL_SIDEBAR", 1)
        storage.set("LS_SIDECAR_TOOLTIP_SHOWN_TRIGGER_PUSH_NOTIFICATION_EXPLANATION", 1)
        storage.set("LS_SIDECAR_TOOLTIP_SHOWN", 1)        

    def navigate_to(self):
        attempts = 0
        selector = TOKEN_IMAGE
        print(TOKEN_IMAGE)
        while attempts < 5:
            try:
                self.driver.get(self.default_url)
                self.hide_popups()
                self.basic_wait(PAGE_LOADER_BIG, False, 5)
                self.basic_wait(PAGE_LOADER_SMALL, False, 5)
                WebDriverWait(self.driver, 5).until(
                    lambda wd: 'bitcoin' in wd.find_element_by_css_selector(selector).get_attribute('class')
                )
            except (TimeoutException, StaleElementReferenceException):
                attempts += 1
            else:
                return
        raise MaxAttemptsLimitException("Exceeded max attempts limit trying to load main page")

    def close_popup(self, selector, timeout):
        try:
            self.basic_wait(selector, True, timeout)
        except TimeoutException:
            return
        button = self.driver.find_element_by_css_selector(selector)
        safe_click(button)
        self.basic_wait(selector, False)

    def close_cookie_popup(self):
        self.close_popup(CLOSE_COOKIE_POPUP_BUTTON, 5)

    def close_explore_popup(self):
        self.close_popup(CLOSE_EXPLORE_POPUP_BUTTON, 15)

    def close_signals_popup(self):
        self.close_popup(CLOSE_SIGNALS_POPUP_BUTTON, 15)

    def get_chart_page(self):
        selector = CHART_PAGE
        return self.driver.find_element_by_css_selector(selector)

    def get_search_dialog(self):
        selector = SEARCH_DIALOG
        return self.driver.find_element_by_css_selector(selector)

    def get_search_dialog_close(self):
        selector = SEARCH_DIALOG_CLOSE
        return self.driver.find_element_by_css_selector(selector)

    def get_search_input(self):
        selector = SEARCH_INPUT
        return self.driver.find_element_by_css_selector(selector)

    def get_search_results(self):
        selector = SEARCH_RESULT
        return self.driver.find_elements_by_css_selector(selector)

    def get_search_result(self, text):
        elements = list(filter(lambda x: text.lower() in x.text.lower(), self.get_search_results()))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException

    def get_search_result_name(self, result):
        selector = SEARCH_RESULT_NAME
        return result.find_element_by_css_selector(selector)

    def get_search_result_ticker(self, result):
        selector = SEARCH_RESULT_TICKER
        return result.find_element_by_css_selector(selector)

    def get_search_noresults(self):
        selector = SEARCH_RESULT_LIST_NO_RESULTS
        return self.driver.find_element_by_css_selector(selector)

    def get_token_selector(self):
        selector = TOKEN_SELECTOR
        return self.find_element_anti_stale(selector)

    def open_search_dialog(self):
        try:
            self.get_search_dialog()
        except NoSuchElementException:
            selector = SEARCH_DIALOG
            safe_click(self.get_token_selector())
            self.basic_wait(selector, True)

    def close_search_dialog(self):
        try:
            self.get_search_dialog()
        except NoSuchElementException:
            pass
        else:
            selector = SEARCH_DIALOG
            close_button = self.get_search_dialog_close()
            safe_click(close_button)
            self.basic_wait(selector, False)

    def get_search_dialog_assets(self):
        selector = SEARCH_DIALOG_ASSET
        return self.driver.find_elements_by_css_selector(selector)

    def get_search_dialog_asset(self, asset):
        elements = list(filter(lambda x: x.text.lower() == asset.lower(), self.get_search_dialog_assets()))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException

    def get_search_dialog_asset_name(self, result):
        selector = SEARCH_DIALOG_ASSET_NAME
        return result.find_element_by_css_selector(selector)

    def get_search_dialog_asset_ticker(self, asset):
        selector = SEARCH_DIALOG_ASSET_TICKER
        return asset.find_element_by_css_selector(selector)

    def search(self, text):
        self.open_search_dialog()
        search_input = self.get_search_input()
        search_input.send_keys(text)
        self.wait.until(
            lambda wd: len(self.get_search_results()) > 0 or self.get_search_noresults().text == "No results found"
        )

    def search_and_select(self, text):
        selector_dialog = SEARCH_DIALOG
        selector_loader = CHART_LOADER
        self.search(text)
        safe_click(self.get_search_result(text))
        self.basic_wait(selector_dialog, False)
        self.basic_wait(selector_loader, False)

    def get_periods(self):
        selector = PERIOD
        return self.driver.find_elements_by_css_selector(selector)

    def get_period(self, period):
        element = next(filter(lambda x: x.text.lower() == period.lower(), self.get_periods()))
        return element

    def get_active_period(self):
        selector = PERIOD_ACTIVE
        return self.driver.find_element_by_css_selector(selector)

    def select_period(self, period):
        selector = CHART_LOADER
        period_selector = self.get_period(period)
        safe_click(period_selector)
        self.wait.until(
            lambda wd: self.get_active_period().text == period
        )
        self.basic_wait(selector, False)

    def get_metrics_menu_button(self):
        selector = METRICS_MENU_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_metrics_menu(self):
        selector = METRICS_MENU
        return self.driver.find_element_by_css_selector(selector)

    def get_metrics_categories(self):
        selector = METRICS_MENU_CATEGORY
        return self.driver.find_elements_by_css_selector(selector)

    def get_metrics_category(self, category):
        elements = list(filter(lambda x: category.lower() in x.text.lower(), self.get_metrics_categories()))
        if elements:
            return elements[0]
        else:
            raise MissingCategoryException(f"Category {category} not found for the selected token")

    def get_metrics_category_active(self):
        selector = METRICS_MENU_CATEGORY_ACTIVE
        return self.driver.find_element_by_css_selector(selector)

    def select_metrics_category(self, category):
        selector = METRICS_MENU_LOADER
        safe_click(self.get_metrics_category(category))
        self.wait.until(
            lambda wd: category.lower() in self.get_metrics_category_active().text.lower()
        )
        self.basic_wait(selector, False)

    def get_metrics(self):
        selector = METRICS_MENU_METRIC
        return self.driver.find_elements_by_css_selector(selector)

    def get_metric(self, metric):
        elements = list(filter(lambda x: metric.lower() in x.text.lower(), self.get_metrics()))
        if elements:
            return elements[0]
        else:
            raise MissingMetricException(f"Metric {metric} not found for the selected token")

    def get_selected_metrics(self):
        selector = METRICS_MENU_METRIC_SELECTED
        return self.driver.find_element_by_css_selector(selector)

    def get_selected_metric(self, metric):
        elements = list(filter(lambda x: x.text.lower() == metric.lower(), self.get_selected_metrics()))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException

    def get_metric_add(self, metric):
        selector = METRICS_MENU_METRIC_ADD
        return metric.find_element_by_css_selector(selector)

    def get_metric_remove(self, metric):
        selector = METRICS_MENU_METRIC_REMOVE
        return metric.find_element_by_css_selector(selector)

    def get_active_metrics(self):
        selector = ACTIVE_METRIC
        return self.driver.find_elements_by_css_selector(selector)

    def get_active_metric(self, metric):
        elements = list(filter(lambda x: x.text.lower() == metric.lower(), self.get_active_metrics()))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException

    def get_active_metric_close(self, active_metric):
        selector = ACTIVE_METRIC_CLOSE
        return active_metric.find_element_by_css_selector(selector)

    def open_metrics_menu(self):
        try:
            self.get_metrics_menu()
        except NoSuchElementException:
            selector_menu = METRICS_MENU
            selector_loader = METRICS_MENU_LOADER
            safe_click(self.get_metrics_menu_button())
            self.basic_wait(selector_menu, True)
            self.basic_wait(selector_loader, False)

    def get_modal_overlay(self):
        selector = MODAL_OVERLAY
        return self.driver.find_element_by_css_selector(selector)

    def close_metrics_menu(self):
        try:
            self.get_metrics_menu()
        except NoSuchElementException:
            pass
        else:
            selector = METRICS_MENU
            safe_click(self.get_modal_overlay())
            self.basic_wait(selector, False)

    def select_metric(self, metric):
        try:
            self.get_active_metric(metric)
        except NoSuchElementException:
            selector = CHART_LOADER
            self.open_metrics_menu()
            self.select_metrics_category(metrics[metric][0])
            metric_element = self.get_metric(metric)
            safe_click(self.get_metric_add(metric_element))
            self.wait.until(
                lambda wd: self.get_active_metric(metric).is_displayed()
            )
            self.basic_wait(selector, False)
            self.close_metrics_menu()

    def select_metrics(self, metrics):
        for metric in metrics:
            self.select_metric(metric)

    def deselect_metric(self, metric):
        try:
            active_metric = self.get_active_metric(metric)
        except NoSuchElementException:
            pass
        else:
            selector = CHART_LOADER
            safe_click(self.get_active_metric_close(active_metric))
            self.wait.until_not(
                lambda wd: self.get_active_metric(metric).is_displayed()
            )
            self.basic_wait(selector, False)


    def clear_active_metrics(self):
        for metric in [x.text for x in self.get_active_metrics()]:
            self.deselect_metric(metric)

    def get_share_dialog(self):
        selector = SHARE_DIALOG
        return self.driver.find_element_by_css_selector(selector)

    def get_share_dialog_link(self):
        selector = SHARE_DIALOG_LINK
        return self.driver.find_element_by_css_selector(selector)

    def get_share_dialog_link_value(self):
        return self.get_share_dialog_link().get_attribute("value")

    def get_share_dialog_close(self):
        selector = SHARE_DIALOG_CLOSE
        return self.driver.find_element_by_css_selector(selector)

    def get_chart_settings_button(self):
        selector = CHART_SETTINGS_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_chart_settings_menu(self):
        selector = CHART_SETTINGS_MENU
        return self.driver.find_element_by_css_selector(selector)

    def get_chart_settings_menu_options(self):
        selector = CHART_SETTINGS_MENU_OPTION
        return self.driver.find_elements_by_css_selector(selector)

    def get_chart_settings_menu_option(self, option_short):
        option = chart_settings_options[option_short]
        element = next(filter(lambda x: x.text.lower() == option.lower(), self.get_chart_settings_menu_options()))
        return element

    def open_chart_settings_menu(self):
        try:
            self.get_chart_settings_menu()
        except NoSuchElementException:
            selector = CHART_SETTINGS_MENU
            safe_click(self.get_chart_settings_button())
            self.basic_wait(selector, True)

    def close_chart_settings_menu(self):
        try:
            self.get_chart_settings_menu()
        except NoSuchElementException:
            pass
        else:
            selector = CHART_SETTINGS_MENU
            safe_click(self.get_modal_overlay())
            self.basic_wait(selector, False)

    def open_share_dialog(self):
        try:
            self.get_share_dialog()
        except NoSuchElementException:
            selector = SHARE_DIALOG
            self.open_chart_settings_menu()
            safe_click(self.get_chart_settings_menu_option("share"))
            self.basic_wait(selector, True)

    def close_share_dialog(self):
        try:
            self.get_share_dialog()
        except NoSuchElementException:
            pass
        else:
            selector = SHARE_DIALOG
            close_button = self.get_share_dialog_close()
            safe_click(close_button)
            self.basic_wait(selector, False)
        finally:
            self.close_chart_settings_menu()

    def get_token_title(self):
        selector = TOKEN_TITLE
        return self.find_element_anti_stale(selector)

    def get_calendar_button(self):
        selector = CALENDAR_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_from_to_dates(self):
        calendar_button = self.get_calendar_button()
        [date_from_text, date_to_text] = calendar_button.text.split('-')
        datetime_from = datetime.strptime(date_from_text.strip(), '%d.%m.%y')
        datetime_to = datetime.strptime(date_to_text.strip(), '%d.%m.%y')
        return datetime_from, datetime_to

    #commented out as element was removed , will delete later if change is permanent
    #def get_interval_button(self):
    #    selector = selectors["interval_button"]
    #    return self.driver.find_element_by_css_selector(selector)

    def get_chart_dates(self):
        selector = CHART_AXIS_DATE
        return self.driver.find_elements_by_css_selector(selector)

    def get_chart_header(self):
        selector = CHART_HEADER
        return self.driver.find_element_by_css_selector(selector)

    def get_token_image(self):
        selector = TOKEN_IMAGE
        return self.find_element_anti_stale(selector)

    def get_token_description(self):
        selector = TOKEN_DESCRIPTION
        return self.find_element_anti_stale(selector)

    def get_token_price(self):
        selector = TOKEN_PRICE
        return self.driver.find_element_by_css_selector(selector)

    def get_token_volume(self):
        selector = TOKEN_VOLUME
        return self.driver.find_element_by_css_selector(selector)

    def get_token_currency(self):
        selector = TOKEN_VOLUME_CURRENCY
        return self.driver.find_element_by_css_selector(selector)

    def get_add_signal_button(self):
        selector = ADD_SIGNAL_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_watch_button(self):
        selector = WATCH_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_account_menu_button(self):
        selector = ACCOUNT_MENU_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def open_account_menu(self):
        selector = ACCOUNT_MENU
        button = self.get_account_menu_button()
        safe_click(button)
        self.basic_wait(selector, True)
