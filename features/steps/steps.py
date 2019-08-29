from behave import *
from main_page import Mainpage
import urllib.parse as urlparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datastorage import *
import time

@Given('I load Santiment stage page')
def step_impl(context):
    context.mainpage = Mainpage(context.browser)
    context.mainpage.navigate_to_main_page()
    context.mainpage.close_cookie_popup()
    context.mainpage.close_explore_popup()

@Then('page title is "{title}"')
def step_impl(context, title):
    assert context.browser.title == title

@Then('I ensure main page is displayed')
def step_impl(context):
    assert context.mainpage.get_page_element().is_displayed() == True

@When('I search for "{text}" in graph search bar')
def step_impl(context, text):
    context.mainpage.search(text)

@When('I search for "{text}" in graph search bar and select the result')
def step_impl(context, text):
    context.mainpage.search_and_select(text)

@When('I select "{period}" period')
def step_impl(context, period):
    context.mainpage.select_period(period)

@When('I select "{category}" category')
def step_impl(context, category):
    context.mainpage.select_metrics_category(category)

@When('I select "{metric}" metric')
def step_impl(context, metric):
    context.mainpage.select_metric(metric)

@When('I deselect "{metric}" metric')
def step_impl(context, metric):
    context.mainpage.deselect_metric(metric)

@When('I open share dialog')
def step_impl(context):
    context.mainpage.open_share_dialog()

@When('I close share dialog')
def step_impl(context):
    context.mainpage.close_share_dialog()

@When('I clear all active metrics')
def step_impl(context):
    context.mainpage.clear_all_active_metrics()

@Then('I verify that share link contains correct data')
def step_impl(context):
    context.mainpage.open_share_dialog()
    link = context.mainpage.get_share_link_value()
    context.mainpage.close_share_dialog()
    parsed = urlparse.urlparse(link)
    netloc = parsed.netloc
    params = urlparse.parse_qs(parsed.query)
    metrics_link = params['metrics'][0].split(',')
    metrics_page = [metrics[metric][1] for metric in context.mainpage.state['active_metrics']]
    title_page = context.mainpage.get_token_title()
    title_link = params['title'][0]
    date_from_page, date_to_page = context.mainpage.get_from_to_dates()
    date_from_page_corrected = date_from_page - relativedelta(days=1)
    date_to_page_corrected = date_to_page - relativedelta(days=1)
    date_from_page_converted = datetime.strftime(date_from_page_corrected, '%Y-%m-%d')
    date_to_page_converted = datetime.strftime(date_to_page_corrected, '%Y-%m-%d')
    date_from_link = params['from'][0].split('T')[0]
    date_to_link = params['to'][0].split('T')[0]
    interval_page = context.mainpage.get_interval()
    interval_link = params['interval'][0]
    assert netloc == 'app-stage.santiment.net'
    assert sorted(metrics_link) == sorted(metrics_page)
    assert title_page == title_link
    assert interval_page == interval_link
    assert date_from_page_converted == date_from_link
    assert date_to_page_converted == date_to_link

@When('I wait for "{sec}" seconds')
def step_impl(context, sec):
    time.sleep(int(sec))
