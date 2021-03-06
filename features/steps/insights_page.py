from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selectors_insights import *
import time
import logging
from datastorage import urls
from constants import BOT_LOGIN_SECRET_ENDPOINT, ENVIRONMENT, BOT_USER_ID
from common_methods import ClickError, MaxAttemptsLimitException, safe_click, set_login_cookie

class TagError(Exception):
    pass

class InsightsPage:

    def __init__(self, driver, is_logged_in):
        self.default_url = urls[ENVIRONMENT]['insights']
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60, ignored_exceptions=[StaleElementReferenceException])
        if is_logged_in:
            set_login_cookie(self.driver)

    def navigate_to(self):
        attempts = 0
        selector = FEATURED_INSIGHTS_TITLE
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

    def close_cookie_popup(self):
        selector = CLOSE_COOKIE_POPUP_BUTTON
        try:
            WebDriverWait(self.driver, 5).until(
                lambda wd: self.driver.find_element_by_css_selector(selector).is_displayed()
            )
        except TimeoutException:
            return
        button = self.driver.find_element_by_css_selector(selector)
        safe_click(button)
        self.wait.until_not(
            lambda wd: self.driver.find_element_by_css_selector(selector).is_displayed()
        )


    def get_write_insight_button(self):
        selector = WRITE_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_tab(self, tab):
        selector = TAB
        element = next(filter(lambda x: x.text == tab, self.driver.find_elements_by_css_selector(selector)))
        return element

    def get_active_tab(self):
        selector = ACTIVE_TAB
        return self.driver.find_element_by_css_selector(selector)

    def get_loader(self):
        selector = LOADER
        return self.driver.find_element_by_css_selector(selector)

    def wait_until_tab_is_active(self, tab):
        self.wait.until_not(
            lambda wd: wd.find_element_by_css_selector(LOADER).is_displayed()
        )
        self.wait.until(
            lambda wd: self.get_active_tab().text == tab
        )

    def activate_tab(self, tab):
        tab_element = self.get_tab(tab)
        safe_click(tab_element)
        self.wait_until_tab_is_active(tab)

    def get_drafts(self):
        selector = DRAFT
        return self.driver.find_elements_by_css_selector(selector)

    def get_delete_draft_button(self, draft):
        selector = DRAFT_DELETE_BUTTON
        return draft.find_element_by_css_selector(selector)

    def get_edit_draft_button(self, draft):
        selector = DRAFT_EDIT_BUTTON
        return draft.find_element_by_css_selector(selector)

    def get_draft(self, i):
        return self.get_drafts()[i]

    def get_draft_title(self, draft):
        selector = DRAFT_TITLE
        return draft.find_element_by_css_selector(selector)

    def get_draft_body(self, draft):
        selector = DRAFT_BODY
        return draft.find_element_by_css_selector(selector)

    def get_draft_timestamp(self, draft):
        selector = DRAFT_TIMESTAMP
        return draft.find_element_by_css_selector(selector)

    def get_delete_draft_dialog(self, draft):
        selector = DRAFT_DELETE_DIALOG
        return self.driver.find_element_by_css_selector(selector)

    def get_delete_draft_cancel_button(self,dialog):
        selector = DRAFT_DELETE_CANCEL
        return dialog.find_element_by_css_selector(selector)

    def get_delete_draft_confirm_button(self, dialog):
        selector = DRAFT_DELETE_CONFIRM
        return dialog.find_element_by_css_selector(selector)

    def delete_draft(self, draft, do_delete):
        number_of_drafts_initial = len(self.get_drafts())
        safe_click(self.get_delete_draft_button(draft))
        self.wait.until(
            lambda wd: self.get_delete_draft_dialog(draft).is_displayed()
        )
        dialog = self.get_delete_draft_dialog(draft)
        button = self.get_delete_draft_confirm_button(dialog) if do_delete else self.get_delete_draft_cancel_button(dialog)
        safe_click(button)
        self.wait.until_not(
            lambda wd: wd.find_element_by_css_selector(DRAFT_DELETE_DIALOG).is_displayed()
        )
        if do_delete:
            self.wait.until(
                lambda wd: len(self.get_drafts()) == number_of_drafts_initial - 1
            )

    def delete_draft_by_index(self, i, do_delete):
        self.delete_draft(self.get_drafts()[i], do_delete)

    def clear_all_drafts(self):
        drafts = self.get_drafts()
        for draft in drafts:
            self.delete_draft(draft, True)

    def edit_draft(self, draft):
        safe_click(self.get_edit_draft_button(draft))
        self.wait.until(
            lambda wd: self.get_editor_title().is_displayed()
        )

    def get_editor_title(self):
        selector = EDITOR_TITLE
        return self.driver.find_element_by_css_selector(selector)

    def get_editor_body(self):
        selector = EDITOR_BODY
        return self.driver.find_element_by_css_selector(selector)

    def get_publish_menu_button(self):
        selector = EDITOR_PUBLISH_MENU_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_tag_input(self):
        selector = EDITOR_TAG_INPUT
        return self.driver.find_element_by_css_selector(selector)

    def get_tag_list_items(self):
        selector = EDITOR_TAG_LIST_ITEM
        return self.driver.find_elements_by_css_selector(selector)

    def get_tag_list_item(self, item):
        element = next(filter(lambda x: x.text.lower() == item.lower(), self.get_tag_list_items()))
        return element

    def get_selected_tags(self):
        selector = EDITOR_SELECTED_TAG
        return self.driver.find_elements_by_css_selector(selector)

    def add_insight_tag(self, tag):
        self.get_tag_input().send_keys(tag)
        self.wait.until(
            lambda wd: tag.lower() in [element.text.lower() for element in self.get_tag_list_items()]
        )
        safe_click(self.get_tag_list_item(tag))
        self.wait.until(
            lambda wd: tag.lower() in [element.text.lower().strip(' \n') for element in self.get_selected_tags()]
        )

    def get_publish_insight_button(self):
        selector = EDITOR_PUBLISH_INSIGHT_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_publish_insight_loader(self):
        selector = EDITOR_PUBLISH_INSIGHT_LOADER
        return self.driver.find_element_by_css_selector(selector)

    def open_publish_menu(self):
        try:
            self.get_publish_insight_button()
        except NoSuchElementException:
            safe_click(self.get_publish_menu_button())
            self.wait.until_not(
                lambda wd: wd.find_element_by_css_selector(EDITOR_PUBLISH_INSIGHT_LOADER).is_displayed()
            )

    def get_draft_saved_timestamp(self):
        selector = EDITOR_SAVED_TIMESTAMP
        return self.driver.find_element_by_css_selector(selector)

    def get_clear_tags_button(self):
        selector = EDITOR_CLEAR_TAGS
        return self.driver.find_element_by_css_selector(selector)

    def clear_tags(self):
        safe_click(self.get_clear_tags_button())
        self.wait.until(
            lambda wd: len(self.get_selected_tags()) == 0
        )
        self.wait.until_not(
            lambda wd: wd.find_element_by_css_selector(EDITOR_PUBLISH_INSIGHT_LOADER).is_displayed()
        )

    def get_tag_list(self):
        selector = EDITOR_TAG_LIST
        return self.driver.find_element_by_css_selector(selector)

    def get_tag_list_toggle(self):
        selector = EDITOR_TAG_LIST_TOGGLE
        return self.driver.find_element_by_css_selector(selector)

    def try_toggle_tag_list(self, state):
        try:
            self.get_tag_list()
            if state:
                return
            else:
                safe_click(self.get_tag_list_toggle())
        except NoSuchElementException:
            if state:
                safe_click(self.get_tag_list_toggle())
            else:
                return

    def is_tag_list_displayed(self):
        try:
            return self.get_tag_list().is_displayed()
        except NoSuchElementException:
            return False

    def toggle_tag_list(self, state):
        self.try_toggle_tag_list(state)
        if state:
            self.wait.until(
                lambda wd: self.get_tag_list().is_displayed()
            )
        else:
            self.wait.until_not(
                lambda wd: self.get_tag_list().is_displayed()
            )

    def open_editor(self):
        try:
            self.get_editor_title()
        except NoSuchElementException:
            safe_click(self.get_write_insight_button())
            self.wait.until(
                lambda wd: self.get_editor_title().is_displayed()
            )

    def write_insight_title(self, title):
        self.get_editor_title().send_keys(title)

    def write_insight_body(self, body):
        safe_click(self.get_editor_body())
        body_input = self.driver.switch_to.active_element
        body_input.send_keys(body)

    def write_insight_tags(self, tags):
        self.open_publish_menu()
        for tag in tags:
            self.add_insight_tag(tag)
        self.wait.until_not(
            lambda wd: wd.find_element_by_css_selector(EDITOR_PUBLISH_INSIGHT_LOADER).is_displayed()
        )

    def publish_insight(self):
        self.open_publish_menu()
        safe_click(self.get_publish_insight_button())
        self.wait.until(
            lambda wd: self.get_active_tab().text == 'My Insights'
        )

    def write_insight(self, title, body, tags):
        if title:
            self.write_insight_title(title)
        if body:
            self.write_insight_body(body)
        if tags and tags[0]:
            self.write_insight_tags(tags)
        if title or body:
            self.wait.until(
                lambda wd: self.get_draft_saved_timestamp().text == 'Draft saved a few seconds ago'
            )

    def write_insight_and_exit(self, title, body, tags, is_published):
        self.open_editor()
        self.write_insight(title, body, tags)
        if is_published:
            self.publish_insight()
        else:
            self.navigate_to()

    def get_read_title(self):
        selector = READ_TITLE
        return self.driver.find_element_by_css_selector(selector)

    def get_read_body(self):
        selector = READ_BODY
        return self.driver.find_element_by_css_selector(selector)

    def get_read_tags(self):
        selector = READ_TAG
        return self.driver.find_elements_by_css_selector(selector)

    def get_read_author(self):
        selector = READ_AUTHOR
        return self.driver.find_element_by_css_selector(selector)

    def get_read_follow_button(self):
        selector = READ_FOLLOW_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_read_timestamp(self):
        selector = READ_TIMESTAMP
        return self.driver.find_element_by_css_selector(selector)

    def get_read_like_button(self):
        selector = READ_LIKE_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_read_share_button(self):
        selector = READ_SHARE_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def get_share_dialog(self):
        selector = SHARE_DIALOG
        return self.driver.find_element_by_css_selector(selector)

    def get_share_dialog_close_button(self):
        selector = SHARE_DIALOG_CLOSE_BUTTON
        return self.driver.find_element_by_css_selector(selector)

    def preview_draft(self, draft):
        draft_title = self.get_draft_title(draft).text
        safe_click(self.get_draft_title(draft))
        self.wait.until(
            lambda wd: self.get_read_title().text == draft_title
        )

    def get_insights(self):
        selector = INSIGHT
        return self.driver.find_elements_by_css_selector(selector)

    def get_insight(self, i):
        return self.get_insights()[i]

    def get_insight_title(self, insight):
        selector = INSIGHT_TITLE
        return insight.find_element_by_css_selector(selector)

    def get_insight_tag_title(self, insight):
        selector = INSIGHT_TAG_TITLE
        return insight.find_element_by_css_selector(selector)

    def has_tag_title(self, insight):
        try:
            return self.get_insight_tag_title(insight)
        except NoSuchElementException:
            return False
        return True

    def get_insight_author(self, insight):
        selector = INSIGHT_AUTHOR
        return insight.find_element_by_css_selector(selector)

    def get_insight_tags(self, insight):
        selector = INSIGHT_TAG
        return insight.find_elements_by_css_selector(selector)

    def get_insight_tag(self, insight, i):
        return self.get_insight_tags(insight)[i]

    def get_insight_timestamp(self, insight):
        selector = INSIGHT_TIMESTAMP
        return insight.find_element_by_css_selector(selector)

    def read_insight(self, insight):
        safe_click(self.get_insight_title(insight))
        self.wait.until(
            lambda wd: self.get_read_title().is_displayed()
        )

    def filter_insights_by_author(self, insight):
        author_element = self.get_insight_author(insight)
        author = author_element.text
        safe_click(author_element)
        self.wait_until_tab_is_active('All Insights')
        return author

    def filter_insights_by_first_tag(self, insight):
        tags = self.get_insight_tags(insight)
        if len(tags) == 0:
            raise TagError("There're no tags on given insight!")
        tag_text = tags[0].text
        safe_click(tags[0])
        self.wait_until_tab_is_active('All Insights')
        return tag_text

    def filter_insights_by_tag(self, insight, tag):
        tags = list(filter(lambda x: x.text.lower() == tag.lower(), self.get_insight_tags(insight)))
        if len(tags) == 0:
            raise TagError(f"There're no '{tag}' tag on given insight!")
        tag_text = tags[0].text
        safe_click(tags[0])
        self.wait_until_tab_is_active('All Insights')
        return tag_text
