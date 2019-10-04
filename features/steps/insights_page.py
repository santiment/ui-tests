from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from datastorage import selectors_insights as selectors
from datastorage import xpaths_insights as xpaths
import time
import logging
from datastorage import urls
from constants import BOT_LOGIN_SECRET_ENDPOINT, ENVIRONMENT
from common_methods import ClickError, MaxAttemptsLimitException, safe_click

class TagError(Exception):
    pass

class InsightsPage:

    def __init__(self, driver, is_logged_in):
        self.default_url = urls[ENVIRONMENT]['insights']
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        if is_logged_in:
            url = urls[ENVIRONMENT]['bot'] + BOT_LOGIN_SECRET_ENDPOINT
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
        except TimeoutException:
            return
        button = self.driver.find_element_by_css_selector(selector)
        safe_click(button)
        self.wait.until_not(
            lambda wd: self.driver.find_element_by_css_selector(selector).is_displayed()
        )


    def get_write_insight_button(self):
        selector = selectors['write_button']
        return self.driver.find_element_by_css_selector(selector)

    def get_tab(self, tab):
        selector = selectors['tab']
        element = next(filter(lambda x: x.text == tab, self.driver.find_elements_by_css_selector(selector)))
        return element

    def get_active_tab(self):
        selector = selectors['active_tab']
        return self.driver.find_element_by_css_selector(selector)

    def get_loader(self):
        selector = selectors['loader']
        return self.driver.find_element_by_css_selector(selector)

    def wait_until_tab_is_active(self, tab):
        self.wait.until_not(
            lambda wd: wd.find_element_by_css_selector(selectors['loader']).is_displayed()
        )
        self.wait.until(
            lambda wd: self.get_active_tab().text == tab
        )

    def activate_tab(self, tab):
        tab_element = self.get_tab(tab)
        safe_click(tab_element)
        self.wait_until_tab_is_active(tab)

    def get_drafts(self):
        selector = selectors['draft']
        return self.driver.find_elements_by_css_selector(selector)

    def get_delete_draft_button(self, draft):
        selector = selectors['draft_delete_button']
        return draft.find_element_by_css_selector(selector)

    def get_edit_draft_button(self, draft):
        selector = selectors['draft_edit_button']
        return draft.find_element_by_css_selector(selector)

    def get_draft(self, i):
        return self.get_drafts()[i]

    def get_draft_title(self, draft):
        selector = selectors['draft_title']
        return draft.find_element_by_css_selector(selector)

    def get_draft_body(self, draft):
        selector = selectors['draft_body']
        return draft.find_element_by_css_selector(selector)

    def get_draft_timestamp(self, draft):
        selector = selectors['draft_timestamp']
        return draft.find_element_by_css_selector(selector)

    def get_delete_draft_dialog(self, draft):
        selector = selectors['draft_delete_dialog']
        return draft.find_element_by_css_selector(selector)

    def get_delete_draft_cancel_button(self,dialog):
        selector = selectors['draft_delete_cancel']
        return dialog.find_element_by_css_selector(selector)

    def get_delete_draft_confirm_button(self, dialog):
        selector = selectors['draft_delete_confirm']
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
            lambda wd: wd.find_element_by_css_selector(selectors['draft_delete_dialog']).is_displayed()
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
        selector = selectors['editor_title']
        return self.driver.find_element_by_css_selector(selector)

    def get_editor_body(self):
        selector = selectors['editor_body']
        return self.driver.find_element_by_css_selector(selector)

    def get_publish_menu_button(self):
        selector = selectors['editor_publish_menu_button']
        return self.driver.find_element_by_css_selector(selector)

    def get_tag_input(self):
        selector = selectors['editor_tag_input']
        return self.driver.find_element_by_css_selector(selector)

    def get_tag_list_items(self):
        selector = selectors['editor_tag_list_item']
        return self.driver.find_elements_by_css_selector(selector)

    def get_tag_list_item(self, item):
        element = next(filter(lambda x: x.text.lower() == item.lower(), self.get_tag_list_items()))
        return element

    def get_selected_tags(self):
        selector = selectors['editor_selected_tag']
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
        selector = selectors['editor_publish_insight_button']
        return self.driver.find_element_by_css_selector(selector)

    def get_publish_insight_loader(self):
        selector = selectors['editor_publish_insight_loader']
        return self.driver.find_element_by_css_selector(selector)

    def open_publish_menu(self):
        try:
            self.get_publish_insight_button()
        except NoSuchElementException:
            safe_click(self.get_publish_menu_button())
            self.wait.until_not(
                lambda wd: wd.find_element_by_css_selector(selectors['editor_publish_insight_loader']).is_displayed()
            )

    def get_draft_saved_timestamp(self):
        selector = selectors['editor_saved_timestamp']
        return self.driver.find_element_by_css_selector(selector)

    def get_clear_tags_button(self):
        selector = selectors['editor_clear_tags']
        return self.driver.find_element_by_css_selector(selector)

    def clear_tags(self):
        safe_click(self.get_clear_tags_button())
        self.wait.until(
            lambda wd: len(self.get_selected_tags()) == 0
        )
        self.wait.until_not(
            lambda wd: wd.find_element_by_css_selector(selectors['editor_publish_insight_loader']).is_displayed()
        )

    def get_tag_list(self):
        selector = selectors['editor_tag_list']
        return self.driver.find_element_by_css_selector(selector)

    def get_tag_list_toggle(self):
        selector = selectors['editor_tag_list_toggle']
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
            lambda wd: wd.find_element_by_css_selector(selectors['editor_publish_insight_loader']).is_displayed()
        )

    def publish_insight(self):
        self.open_publish_menu()
        safe_click(self.get_publish_insight_button())
        self.wait.until(
            lambda wd: self.get_active_tab().text == 'My Insights'
        )

    def write_insight(self, title, body, tags, is_published):
        self.open_editor()
        self.write_insight_title(title)
        self.write_insight_body(body)
        self.write_insight_tags(tags)
        if is_published:
            self.publish_insight()
        else:
            self.navigate_to()

    def get_read_title(self):
        selector = selectors['read_title']
        return self.driver.find_element_by_css_selector(selector)

    def get_read_body(self):
        selector = selectors['read_body']
        return self.driver.find_element_by_css_selector(selector)

    def get_read_tags(self):
        selector = selectors['read_tag']
        return self.driver.find_elements_by_css_selector(selector)

    def get_read_author(self):
        selector = selectors['read_author']
        return self.driver.find_element_by_css_selector(selector)

    def get_read_follow_button(self):
        selector = selectors['read_follow_button']
        return self.driver.find_element_by_css_selector(selector)

    def get_read_timestamp(self):
        selector = selectors['read_timestamp']
        return self.driver.find_element_by_css_selector(selector)

    def get_read_like_button(self):
        selector = selectors['read_like_button']
        return self.driver.find_element_by_css_selector(selector)

    def get_read_share_button(self):
        selector = selectors['read_share_button']
        return self.driver.find_element_by_css_selector(selector)

    def get_share_dialog(self):
        selector = selectors['share_dialog']
        return self.driver.find_element_by_css_selector(selector)

    def get_share_dialog_close_button(self):
        selector = selectors['share_dialog_close_button']
        return self.driver.find_element_by_css_selector(selector)

    def preview_draft(self, draft):
        draft_title = self.get_draft_title(draft).text
        safe_click(self.get_draft_title(draft))
        self.wait.until(
            lambda wd: self.get_read_title().text == draft_title
        )

    def get_insights(self):
        selector = selectors['insight']
        return self.driver.find_elements_by_css_selector(selector)

    def get_insight(self, i):
        return self.get_insights()[i]

    def get_insight_title(self, insight):
        selector = selectors['insight_title']
        return insight.find_element_by_css_selector(selector)

    def get_insight_author(self, insight):
        selector = selectors['insight_author']
        return insight.find_element_by_css_selector(selector)

    def get_insight_tags(self, insight):
        selector = selectors['insight_tag']
        return insight.find_elements_by_css_selector(selector)

    def get_insight_tag(self, insight, i):
        return self.get_insight_tags(insight)[i]

    def get_insight_timestamp(self, insight):
        selector = selectors['insight_timestamp']
        return insight.find_element_by_css_selector(selector)

    def read_insight(self, draft):
        safe_click(self.get_draft_title(draft))
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
