from behave import *
from main_page import Mainpage
import urllib.parse as urlparse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datastorage import metrics, selectors, xpaths, chart_settings_options, delta, bot_url, title_conversion
import time

@Given('I load Santiment stage page and "{is_logged_in_str}" log in')
def step_impl(context, is_logged_in_str):
    is_logged_in = is_logged_in_str == 'do'
    context.mainpage = Mainpage(context.browser, is_logged_in)
    context.mainpage.navigate_to_main_page()
    context.mainpage.close_cookie_popup()
    context.mainpage.close_explore_popup()

@Then('page title is "{title}"')
def step_impl(context, title):
    assert context.browser.title == title

@Then('I ensure main page is displayed')
def step_impl(context):
    assert context.mainpage.get_chart_page_element().is_displayed() == True

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

@When('I select "{metrics}" metrics')
def step_impl(context, metrics):
    metrics_list = [x.strip() for x in metrics.split(',')]
    for metric in metrics_list:
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
    metrics_page = [metrics[metric][1] for metric in context.mainpage.get_all_active_metrics()]
    title_page = context.mainpage.get_token_title()
    if title_page in title_conversion:
        title_page = title_conversion[title_page]
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

@Then('I verify that chart dates are correct for "{period}" period')
def step_impl(context, period):
    if period not in delta:
        raise ValueError("Unknown period: {0}".format(period))
    date_pattern = '%d %b %y'
    end_date = datetime.combine(datetime.today().date(), datetime.min.time())
    start_date = end_date - delta[period][0]
    start_date_graph = datetime.strptime(context.mainpage.get_chart_date('first'), date_pattern)
    end_date_graph = datetime.strptime(context.mainpage.get_chart_date('last'), date_pattern)
    assert abs(end_date - end_date_graph) < timedelta(days=2)
    if period != 'all':
        assert abs(start_date - start_date_graph) < delta[period][1]


@Then('I verify that calendar dates are correct for "{period}" period')
def step_impl(context, period):
    if period not in delta:
        raise ValueError("Unknown period: {0}".format(period))
    end_date = datetime.today() + relativedelta(days=1)
    start_date = datetime.today() - delta[period][0]
    start_date_cal, end_date_cal = context.mainpage.get_from_to_dates()
    assert end_date.date() == end_date_cal.date()
    if period != 'all':
        assert start_date.date() == start_date_cal.date()

@Then('I verify that token info is displayed correctly')
def step_impl(context):
    token_title_element = context.mainpage.get_token_title_element()
    token_image_element = context.mainpage.get_token_image_element()
    token_price_element = context.mainpage.get_token_price_element()
    token_volume_element = context.mainpage.get_token_volume_element()
    token_currency_element = context.mainpage.get_token_currency_element()
    add_signal_button = context.mainpage.get_add_signal_button()
    watch_button = context.mainpage.get_watch_button()

    assert token_title_element.is_displayed()
    assert token_price_element.is_displayed()
    assert token_volume_element.is_displayed()
    assert token_currency_element.is_displayed()
    assert add_signal_button.is_displayed()
    assert watch_button.is_displayed()


    title = token_title_element.text
    nickname = title.split(' ')[-1]
    for x in '() ':
        nickname = nickname.replace(x, '')
    first_name = title.split(' ')[0].lower()

    assert nickname == token_currency_element.text
    assert first_name in token_image_element.get_attribute("class")
    assert watch_button.text == "Watch {0}".format(nickname)
    assert add_signal_button.text == "Add signal"

    token_price_digits = token_price_element.text
    token_volume_digits = token_volume_element.text
    for x in '$.,0 ':
        token_price_digits = token_price_digits.replace(x, '')
        token_volume_digits = token_volume_digits.replace(x, '')

    assert token_price_digits != ''
    assert token_volume_digits != ''

@When("I open account menu")
def step_impl(context):
    account_menu = context.mainpage.open_account_menu()

@Then('I verify that "{period}" period is selected')
def step_impl(context, period):
    active_period_element = context.mainpage.get_active_period_element()
    assert active_period_element.text == period

@Then('I verify that "{metric}" metric is active')
def step_impl(context, metric):
    active_metric_elements = context.mainpage.get_all_active_metric_elements()
    assert metric in [element.text for element in active_metric_elements]

@Then('I verify that "{metrics}" metrics are active')
def step_impl(context, metrics):
    metric_list = [x.strip() for x in metrics.split(',')]
    active_metric_elements = context.mainpage.get_all_active_metric_elements()
    active_metric_names = [element.text for element in active_metric_elements]
    assert sorted(metric_list) == sorted(active_metric_names)
