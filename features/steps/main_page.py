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
from datastorage import selectors_main as selectors
from datastorage import metrics, chart_settings_options, delta, title_conversion, urls
from constants import BOT_LOGIN_SECRET_ENDPOINT, ENVIRONMENT, CONFIG_FILE, BOT_USER_ID
from common_methods import ClickError, MaxAttemptsLimitException, safe_click, set_login_cookie

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

    def navigate_to(self):
        attempts = 0
        selector = selectors["token_image"]
        while attempts < 5:
            try:
                self.driver.get(self.default_url)
                self.basic_wait(selectors["page_loader_big"], False, 5)
                self.basic_wait(selectors["page_loader_small"], False, 5)
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
        self.close_popup(selectors["close_cookie_popup_button"], 5)

    def close_explore_popup(self):
        self.close_popup(selectors["close_explore_popup_button"], 15)

    def close_signals_popup(self):
        self.close_popup(selectors["close_signals_popup_button"], 15)

    def get_chart_page(self):
        selector = selectors["chart_page"]
        return self.driver.find_element_by_css_selector(selector)

    def get_search_dialog(self):
        selector = selectors["search_dialog"]
        return self.driver.find_element_by_css_selector(selector)

    def get_search_dialog_close(self):
        selector = selectors["search_dialog_close"]
        return self.driver.find_element_by_css_selector(selector)

    def get_search_input(self):
        selector = selectors["search_input"]
        return self.driver.find_element_by_css_selector(selector)

    def get_search_results(self):
        selector = selectors["search_result"]
        return self.driver.find_elements_by_css_selector(selector)

    def get_search_result(self, text):
        elements = list(filter(lambda x: text.lower() in x.text.lower(), self.get_search_results()))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException

    def get_search_result_name(self, result):
        selector = selectors["search_result_name"]
        return result.find_element_by_css_selector(selector)

    def get_search_result_ticker(self, result):
        selector = selectors["search_result_ticker"]
        return result.find_element_by_css_selector(selector)

    def get_search_noresults(self):
        selector = selectors["search_result_list_no_results"]
        return self.driver.find_element_by_css_selector(selector)

    def get_token_selector(self):
        selector = selectors["token_selector"]
        return self.find_element_anti_stale(selector)

    def open_search_dialog(self):
        try:
            self.get_search_dialog()
        except NoSuchElementException:
            selector = selectors["search_dialog"]
            safe_click(self.get_token_selector())
            self.basic_wait(selector, True)

    def close_search_dialog(self):
        try:
            self.get_search_dialog()
        except NoSuchElementException:
            pass
        else:
            selector = selectors["search_dialog"]
            close_button = self.get_search_dialog_close()
            safe_click(close_button)
            self.basic_wait(selector, False)

    def get_search_dialog_assets(self):
        selector = selectors["search_dialog_asset"]
        return self.driver.find_elements_by_css_selector(selector)

    def get_search_dialog_asset(self, asset):
        elements = list(filter(lambda x: x.text.lower() == asset.lower(), self.get_search_dialog_assets()))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException

    def get_search_dialog_asset_name(self, result):
        selector = selectors["search_dialog_asset_name"]
        return result.find_element_by_css_selector(selector)

    def get_search_dialog_asset_ticker(self, asset):
        selector = selectors["search_dialog_asset_ticker"]
        return asset.find_element_by_css_selector(selector)

    def search(self, text):
        self.open_search_dialog()
        search_input = self.get_search_input()
        search_input.send_keys(text)
        self.wait.until(
            lambda wd: len(self.get_search_results()) > 0 or self.get_search_noresults().text == "No results found"
        )

    def search_and_select(self, text):
        selector_dialog = selectors["search_dialog"]
        selector_loader = selectors['chart_loader']
        self.search(text)
        safe_click(self.get_search_result(text))
        self.basic_wait(selector_dialog, False)
        self.basic_wait(selector_loader, False)

    def get_periods(self):
        selector = selectors["period"]
        return self.driver.find_elements_by_css_selector(selector)

    def get_period(self, period):
        element = next(filter(lambda x: x.text.lower() == period.lower(), self.get_periods()))
        return element

    def get_active_period(self):
        selector = selectors["period_active"]
        return self.driver.find_element_by_css_selector(selector)

    def select_period(self, period):
        selector = selectors["chart_loader"]
        period_selector = self.get_period(period)
        safe_click(period_selector)
        self.wait.until(
            lambda wd: self.get_active_period().text == period
        )
        self.basic_wait(selector, False)

    def get_metrics_menu_button(self):
        selector = selectors["metrics_menu_button"]
        return self.driver.find_element_by_css_selector(selector)

    def get_metrics_menu(self):
        selector = selectors["metrics_menu"]
        return self.driver.find_element_by_css_selector(selector)

    def get_metrics_categories(self):
        selector = selectors["metrics_menu_category"]
        return self.driver.find_elements_by_css_selector(selector)

    def get_metrics_category(self, category):
        elements = list(filter(lambda x: category.lower() in x.text.lower(), self.get_metrics_categories()))
        if elements:
            return elements[0]
        else:
            raise MissingCategoryException(f"Category {category} not found for the selected token")

    def get_metrics_category_active(self):
        selector = selectors["metrics_menu_category_active"]
        return self.driver.find_element_by_css_selector(selector)

    def select_metrics_category(self, category):
        selector = selectors["metrics_menu_loader"]
        safe_click(self.get_metrics_category(category))
        self.wait.until(
            lambda wd: category.lower() in self.get_metrics_category_active().text.lower()
        )
        self.basic_wait(selector, False)

    def get_metrics(self):
        selector = selectors["metrics_menu_metric"]
        return self.driver.find_elements_by_css_selector(selector)

    def get_metric(self, metric):
        elements = list(filter(lambda x: metric.lower() in x.text.lower(), self.get_metrics()))
        if elements:
            return elements[0]
        else:
            raise MissingMetricException(f"Metric {metric} not found for the selected token")

    def get_selected_metrics(self):
        selector = selectors["metrics_menu_metric_selected"]
        return self.driver.find_element_by_css_selector(selector)

    def get_selected_metric(self, metric):
        elements = list(filter(lambda x: x.text.lower() == metric.lower(), self.get_selected_metrics()))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException

    def get_metric_add(self, metric):
        selector = selectors["metrics_menu_metric_add"]
        return metric.find_element_by_css_selector(selector)

    def get_metric_remove(self, metric):
        selector = selectors["metrics_menu_metric_remove"]
        return metric.find_element_by_css_selector(selector)

    def get_active_metrics(self):
        selector = selectors["active_metric"]
        return self.driver.find_elements_by_css_selector(selector)

    def get_active_metric(self, metric):
        elements = list(filter(lambda x: x.text.lower() == metric.lower(), self.get_active_metrics()))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException

    def get_active_metric_close(self, active_metric):
        selector = selectors["active_metric_close"]
        return active_metric.find_element_by_css_selector(selector)

    def open_metrics_menu(self):
        try:
            self.get_metrics_menu()
        except NoSuchElementException:
            selector_menu = selectors['metrics_menu']
            selector_loader = selectors['metrics_menu_loader']
            safe_click(self.get_metrics_menu_button())
            self.basic_wait(selector_menu, True)
            self.basic_wait(selector_loader, False)

    def get_modal_overlay(self):
        selector = selectors["modal_overlay"]
        return self.driver.find_element_by_css_selector(selector)

    def close_metrics_menu(self):
        try:
            self.get_metrics_menu()
        except NoSuchElementException:
            pass
        else:
            selector = selectors["metrics_menu"]
            safe_click(self.get_modal_overlay())
            self.basic_wait(selector, False)

    def select_metric(self, metric):
        try:
            self.get_active_metric(metric)
        except NoSuchElementException:
            selector = selectors['chart_loader']
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
            selector = selectors['chart_loader']
            safe_click(self.get_active_metric_close(active_metric))
            self.wait.until_not(
                lambda wd: self.get_active_metric(metric).is_displayed()
            )
            self.basic_wait(selector, False)


    def clear_active_metrics(self):
        for metric in [x.text for x in self.get_active_metrics()]:
            self.deselect_metric(metric)

    def get_share_dialog(self):
        selector = selectors["share_dialog"]
        return self.driver.find_element_by_css_selector(selector)

    def get_share_dialog_link(self):
        selector = selectors["share_dialog_link"]
        return self.driver.find_element_by_css_selector(selector)

    def get_share_dialog_link_value(self):
        return self.get_share_dialog_link().get_attribute("value")

    def get_share_dialog_close(self):
        selector = selectors["share_dialog_close"]
        return self.driver.find_element_by_css_selector(selector)

    def get_chart_settings_button(self):
        selector = selectors["chart_settings_button"]
        return self.driver.find_element_by_css_selector(selector)

    def get_chart_settings_menu(self):
        selector = selectors["chart_settings_menu"]
        return self.driver.find_element_by_css_selector(selector)

    def get_chart_settings_menu_options(self):
        selector = selectors["chart_settings_menu_option"]
        return self.driver.find_elements_by_css_selector(selector)

    def get_chart_settings_menu_option(self, option_short):
        option = chart_settings_options[option_short]
        element = next(filter(lambda x: x.text.lower() == option.lower(), self.get_chart_settings_menu_options()))
        return element

    def open_chart_settings_menu(self):
        try:
            self.get_chart_settings_menu()
        except NoSuchElementException:
            selector = selectors["chart_settings_menu"]
            safe_click(self.get_chart_settings_button())
            self.basic_wait(selector, True)

    def close_chart_settings_menu(self):
        try:
            self.get_chart_settings_menu()
        except NoSuchElementException:
            pass
        else:
            selector = selectors["chart_settings_menu"]
            safe_click(self.get_modal_overlay())
            self.basic_wait(selector, False)

    def open_share_dialog(self):
        try:
            self.get_share_dialog()
        except NoSuchElementException:
            selector = selectors["share_dialog"]
            self.open_chart_settings_menu()
            safe_click(self.get_chart_settings_menu_option("share"))
            self.basic_wait(selector, True)

    def close_share_dialog(self):
        try:
            self.get_share_dialog()
        except NoSuchElementException:
            pass
        else:
            selector = selectors["share_dialog"]
            close_button = self.get_share_dialog_close()
            safe_click(close_button)
            self.basic_wait(selector, False)
        finally:
            self.close_chart_settings_menu()

    def get_token_title(self):
        selector = selectors["token_title"]
        return self.find_element_anti_stale(selector)

    def get_calendar_button(self):
        selector = selectors["calendar_button"]
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
        selector = selectors["chart_axis_date"]
        return self.driver.find_elements_by_css_selector(selector)

    def get_chart_header(self):
        selector = selectors["chart_header"]
        return self.driver.find_element_by_css_selector(selector)

    def get_token_image(self):
        selector = selectors["token_image"]
        return self.find_element_anti_stale(selector)

    def get_token_description(self):
        selector = selectors["token_description"]
        return self.find_element_anti_stale(selector)

    def get_token_price(self):
        selector = selectors["token_price"]
        return self.driver.find_element_by_css_selector(selector)

    def get_token_volume(self):
        selector = selectors["token_volume"]
        return self.driver.find_element_by_css_selector(selector)

    def get_token_currency(self):
        selector = selectors["token_volume_currency"]
        return self.driver.find_element_by_css_selector(selector)

    def get_add_signal_button(self):
        selector = selectors["add_signal_button"]
        return self.driver.find_element_by_css_selector(selector)

    def get_watch_button(self):
        selector = selectors["watch_button"]
        return self.driver.find_element_by_css_selector(selector)

    def get_account_menu_button(self):
        selector = selectors["account_menu_button"]
        return self.driver.find_element_by_css_selector(selector)

    def open_account_menu(self):
        selector = selectors["account_menu"]
        button = self.get_account_menu_button()
        safe_click(button)
        self.basic_wait(selector, True)
