from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from datastorage import selectors_insights as selectors
from datastorage import xpaths_insights as xpaths
from datastorage import bot_url, urls
from constants import BOT_LOGIN_SECRET_ENDPOINT, ENVIRONMENT
from common_methods import ClickError, MaxAttemptsLimitException, safe_click


class InsightsPage:

    def __init__(self, driver, is_logged_in):
        self.default_url = urls[ENVIRONMENT]['insights']
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)
        if is_logged_in:
            url = bot_url + BOT_LOGIN_SECRET_ENDPOINT
            self.driver.get(url)

    def navigate_to(self):
        attempts = 0
        selector = selectors["featured_insights_title"]
        while attempts < 5:
            try:
                self.driver.get(self.default_url)
                self.wait.until(
                    lambda wd: wd.find_element_by_css_selector(selector).text == "Featured insights"
                )
                return
            except TimeoutException:
                attempts += 1
        raise MaxAttemptsLimitException("Exceeded max attempts limit trying to load Insights page")

    def close_cookie_popup(self):
        selector = selectors["close_cookie_popup_button"]
        try:
            self.wait.until(
                lambda wd: self.driver.find_element_by_css_selector(selector).is_displayed()
            )
            button = self.driver.find_element_by_css_selector(selector)
            safe_click(button)
            self.wait.until(
                lambda wd: self.driver.find_element_by_css_selector(selector).is_displayed() == False
            )
        except TimeoutException:
            pass

    def get_write_insight_button(self):
        selector = selectors['write_button']
        return self.driver.find_element_by_css_selector(selector)

    def get_tab(self, tab):
        selector = selectors['tab']
        selector_active = selectors['active_tab']
        element = next(filter(lambda x: x.text == tab, self.driver.find_elements_by_css_selector(selector)))
        return element

    def get_active_tab(self):
        selector = selectors['active_tab']
        return self.driver.find_element_by_css_selector(selector)

    def activate_tab(self, tab):
        selector_loader = selectors['loader']
        selector_active = selectors['active_tab']
        tab_element = self.get_tab(tab)
        safe_click(tab_element)
        self.wait.until(
            lambda wd: wd.find_element_by_css_selector(selector_loader).is_displayed() == False
        )
        self.wait.until(
            lambda wd: wd.find_element_by_css_selector(selector_active).text == tab
        )

    def get_draft_elements(self):
        selector = selectors['draft']
        return self.driver.find_elements_by_css_selector(selector)

    def get_delete_draft_button(self, draft):
        selector = selectors['delete_draft_button']
        return draft.find_element_by_css_selector(selector)

    def get_edit_draft_button(self, draft):
        selector = selectors['edit_draft_button']
        return draft.find_element_by_css_selector(selector)

    def get_last_draft(self):
        return self.get_draft_elements()[0]
