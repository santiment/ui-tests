from behave import *
from main_page import Mainpage
from insights_page import InsightsPage
import urllib.parse as urlparse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datastorage import metrics, delta, title_conversion, can_cant, do_dont, insights_filter_options, insights_length_options, have_havent
import time
from constants import ENVIRONMENT
import uuid
import parse

@parse.with_pattern(r"[\w ,]+")
def parse_string(text):
     return text.strip()

register_type(Name=parse_string)
use_step_matcher("cfparse")

#given steps
@Given('I load Santiment main page and "{is_logged_in_str}" log in')
def step_impl(context, is_logged_in_str):
    is_logged_in = is_logged_in_str == 'do'
    context.mainpage = Mainpage(context.browser, is_logged_in)
    context.mainpage.navigate_to()
    context.mainpage.close_cookie_popup()
    context.mainpage.close_explore_popup()
    context.mainpage.close_signals_popup()


@Given('I load Santiment Insights page and "{is_logged_in_str}" log in')
def step_impl(context, is_logged_in_str):
    is_logged_in = is_logged_in_str == 'do'
    context.insights_page = InsightsPage(context.browser, is_logged_in)
    context.insights_page.navigate_to()
    context.insights_page.close_cookie_popup()

#when then steps related to Main page
@Then('page title is "{title}"')
def step_impl(context, title):
    assert context.browser.title == title

@Then('I ensure main page is displayed')
def step_impl(context):
    assert context.mainpage.get_chart_page().is_displayed() == True

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
    context.mainpage.select_metrics(metrics_list)

@When('I deselect "{metric}" metric')
def step_impl(context, metric):
    context.mainpage.deselect_metric(metric)

@When('I open share dialog')
def step_impl(context):
    context.mainpage.open_share_dialog()

@When('I close share dialog')
def step_impl(context):
    context.mainpage.close_share_dialog()

@When('I clear active metrics')
def step_impl(context):
    context.mainpage.clear_active_metrics()

@Then('I verify that share link contains correct data')
def step_impl(context):
    context.mainpage.open_share_dialog()
    link = context.mainpage.get_share_dialog_link_value()
    context.mainpage.close_share_dialog()
    parsed = urlparse.urlparse(link)
    netloc = parsed.netloc
    params = urlparse.parse_qs(parsed.query)
    metrics_link = params['metrics'][0].split(',')
    metrics_page = [metrics[metric.text][1] for metric in context.mainpage.get_active_metrics()]
    title_page = context.mainpage.get_token_title().text
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
    interval_page = context.mainpage.get_interval_button().text
    interval_link = params['interval'][0]
    netloc_expected = 'app-stage.santiment.net' if ENVIRONMENT == 'stage' else 'app.santiment.net'
    print(title_page, title_link)
    print(metrics_page, metrics_link)
    assert netloc == netloc_expected
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
    start_date_graph = datetime.strptime(context.mainpage.get_chart_dates()[0].text, date_pattern)
    end_date_graph = datetime.strptime(context.mainpage.get_chart_dates()[-1].text, date_pattern)
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
    token_price_element = context.mainpage.get_token_price()
    token_volume_element = context.mainpage.get_token_volume()
    token_currency_element = context.mainpage.get_token_currency()
    add_signal_button = context.mainpage.get_add_signal_button()
    watch_button = context.mainpage.get_watch_button()

    assert context.mainpage.get_token_title().is_displayed()
    assert context.mainpage.get_token_image().is_displayed()
    assert token_price_element.is_displayed()
    assert token_volume_element.is_displayed()
    assert token_currency_element.is_displayed()
    assert add_signal_button.is_displayed()
    assert watch_button.is_displayed()


    title = context.mainpage.get_token_title().text
    nickname = title.split(' ')[-1]
    for x in '() ':
        nickname = nickname.replace(x, '')
    first_name = title.split(' ')[0].lower()

    assert nickname == token_currency_element.text
    assert first_name in context.mainpage.get_token_image().get_attribute("class")
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
    active_period_element = context.mainpage.get_active_period()
    assert active_period_element.text == period

@Then('I verify that "{metric}" metric is active')
def step_impl(context, metric):
    active_metrics = context.mainpage.get_active_metrics()
    assert metric in [element.text for element in active_metrics]

@Then('I verify that "{metrics}" metrics are active')
def step_impl(context, metrics):
    metric_list = [x.strip() for x in metrics.split(',')]
    active_metrics = context.mainpage.get_active_metrics()
    active_metric_names = [element.text for element in active_metrics]
    assert sorted(metric_list) == sorted(active_metric_names)

#when then steps related to Insights page
@Then('I verify Insights page is displayed')
def step_impl(context):
    assert context.insights_page.get_write_insight_button().text == "Write insight"

@When('I activate "{tab}" tab')
def step_impl(context, tab):
    context.insights_page.activate_tab(tab)

@Then('I verify "{tab}" tab is active')
def step_impl(context, tab):
    assert tab == context.insights_page.get_active_tab().text

@When('I save unique Insight title and body')
def step_impl(context):
    context.insights_page.unique_title_short = str(uuid.uuid1())[:5]
    context.insights_page.unique_body_short = str(uuid.uuid1())[:5]
    context.insights_page.unique_title_long = str(uuid.uuid1())[:6]
    context.insights_page.unique_body_long = str(uuid.uuid1())[:6]

@When('I write Insight with "{title:Name?}" title, "{body:Name?}" body, "{tags_str:Name?}" tags and stay in Editor')
def step_impl(context, title='', body='', tags_str=''):
    tags = [x.strip() for x in tags_str.split(',')] if tags_str else []
    context.insights_page.open_editor()
    context.insights_page.write_insight(title, body, tags)

@When('I write Insight with unique {title_length} title, {body_length} body, "{tags_str:Name?}" tags and {do_publish} publish it')
def step_impl(context, title_length, body_length, tags_str, do_publish):
    if do_publish not in do_dont:
        raise ValueError(f"do_publish field can only take values from {do_dont}")
    if title_length not in insights_length_options:
        raise ValueError(f"title_length field can only take values from {insights_length_options}")
    if body_length not in insights_length_options:
        raise ValueError(f"body_length field can only take values from {insights_length_options}")
    if title_length == 'long':
        title = context.insights_page.unique_title_long
    elif title_length == 'short':
        title = context.insights_page.unique_title_short
    else:
        title = ''
    if body_length == 'long':
        body = context.insights_page.unique_body_long
    elif body_length == 'short':
        body = context.insights_page.unique_body_short
    else:
        body = ''
    tags = [x.strip() for x in tags_str.split(',')] if tags_str else []
    is_published = do_publish == 'do'
    context.insights_page.write_insight_and_exit(title, body, tags, is_published)
    context.insights_page.last_saved_title = title
    context.insights_page.last_saved_body = body
    context.insights_page.last_saved_tags = tags

@Then('I verify I {can_publish} publish the Insight')
def step_impl(context, can_publish):
    if can_publish not in can_cant:
        raise ValueError(f"can_publish field can only take values from {can_cant}")
    is_disabled = 'disabled' in context.insights_page.get_publish_menu_button().get_attribute("class")
    print(is_disabled)
    print(can_publish != 'can')
    assert is_disabled == (can_publish != 'can')

@Then('I verify I {can_add} add more tags')
def step_impl(context, can_add):
    if can_add not in can_cant:
        raise ValueError(f"can_add field can only take values from {can_cant}")
    can_add_bool = can_add == 'can'
    context.insights_page.try_toggle_tag_list(True)
    assert context.insights_page.is_tag_list_displayed() == can_add_bool

@Then('I verify the latest draft {does_have} latest saved title and body')
def step_impl(context, does_have):
    if does_have not in have_havent:
        raise ValueError(f"does_have field can only take values from {have_havent}")
    does_have_bool = does_have == 'has'
    draft = context.insights_page.get_draft(0)
    title = context.insights_page.get_draft_title(draft).text
    body = context.insights_page.get_draft_body(draft).text
    print(f'actual {title} expected', context.insights_page.last_saved_title)
    title_match = title == context.insights_page.last_saved_title
    print(f'actual {body} expected', context.insights_page.last_saved_body)
    body_match = body == context.insights_page.last_saved_body
    final_match = title_match and body_match
    assert final_match == does_have_bool

@Then('I verify the latest Insight {does_have} latest saved title, tags and tag title')
def step_impl(context, does_have):
    if does_have not in have_havent:
        raise ValueError(f"does_have field can only take values from {have_havent}")
    does_have_bool = does_have == 'has'
    insight = context.insights_page.get_insight(0)
    title = context.insights_page.get_insight_title(insight).text
    tags = [x.text for x in context.insights_page.get_insight_tags(insight)]
    title_match = title == context.insights_page.last_saved_title
    tags_match = sorted(tags) == sorted(context.insights_page.last_saved_tags)
    final_match = title_match and tags_match
    if tags and context.insights_page.has_tag_title(insight):
        tag_title = context.insights_page.get_insight_tag_title(insight).text
        final_match = final_match and tag_title.lower() == f'{tags[0]} price since publication'
    assert final_match == does_have_bool

@When('I preview the latest draft')
def step_impl(context):
    draft = context.insights_page.get_draft(0)
    context.insights_page.preview_draft(draft)

@When('I read the latest Insight')
def step_impl(context):
    insight = context.insights_page.get_insight(0)
    context.insights_page.read_insight(insight)

@Then('I verify read page {does_have} latest saved title, body and tags')
def step_impl(context, does_have):
    if does_have not in have_havent:
        raise ValueError(f"does_have field can only take values from {have_havent}")
    does_have_bool = does_have == 'has'
    title = context.insights_page.get_read_title().text
    body = context.insights_page.get_read_body().text
    tags = [x.text for x in context.insights_page.get_read_tags()]
    print(title, context.insights_page.last_saved_title)
    title_match = title == context.insights_page.last_saved_title
    print(body, context.insights_page.last_saved_body)
    body_match = body == context.insights_page.last_saved_body
    print(sorted(tags), sorted(context.insights_page.last_saved_tags))
    tags_match = sorted(tags) == sorted(context.insights_page.last_saved_tags)
    final_match = title_match and body_match and tags_match
    assert does_have_bool == final_match

@When('I filter Insights by {filter_option} of the latest Insight')
def step_impl(context, filter_option):
    if filter_option not in insights_filter_options:
        raise ValueError(f"filter_option field can only take values from {insights_filter_options}")
    insight = context.insights_page.get_insight(0)
    if filter_option == 'author':
        context.insights_page.filtered_by_author = context.insights_page.filter_insights_by_author(insight)
    else:
        context.insights_page.filtered_by_tag = context.insights_page.filter_insights_by_first_tag(insight)

@Then('I verify Insights are filtered by {filter_option}')
def step_impl(context, filter_option):
    if filter_option not in insights_filter_options:
        raise ValueError(f"filter_option field can only take values from {insights_filter_options}")
    insights = context.insights_page.get_insights()
    for insight in insights:
        if filter_option == 'author':
            assert context.insights_page.filtered_by_author == context.insights_page.get_insight_author(insight).text
        else:
            assert context.insights_page.filtered_by_tag in [x.text for x in context.insights_page.get_insight_tags(insight)]

@When('I clear all drafts')
def step_impl(context):
    context.insights_page.clear_all_drafts()

@When('I do stuff')
def step_impl(context):
    context.insights_page.write_insight_and_exit('test title', 'test body', ['san', 'btc'], True)
    #insight = context.insights_page.get_insight(0)
    #author = context.insights_page.filter_insights_by_author(insight)
    #insights_filtered = context.insights_page.get_insights()
    #for insight in insights_filtered:
    #    assert context.insights_page.get_insight_author(insight).text == author
    #context.insights_page.activate_tab('All Insights')
    #insight = context.insights_page.get_insight(0)
    #tag = context.insights_page.filter_insights_by_first_tag(insight)
    #insights_filtered = context.insights_page.get_insights()
    #for insight in insights_filtered:
    #    assert tag in [x.text for x in context.insights_page.get_insight_tags(insight)]
