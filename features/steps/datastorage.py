from dateutil.relativedelta import relativedelta
from datetime import timedelta

metrics = {
    "Price": ("Financial", "historyPrice"),
    "Volume": ("Financial", "volume"),
    "Development Activity": ("Development", "devActivity"),
    "Twitter": ("Social", "historyTwitterData"),
    "Social Volume": ("Social", "socialVolume"),
    "Social Dominance": ("Social", "socialDominance"),
    "Daily Active Deposits": ("On-chain",),
    "Exchange Flow Balance": ("On-chain", "exchangeFundsFlow"),
    "Eth Spent Over Time": ("On-chain", "ethSpentOverTime"),
    "In Top Holders Total": ("On-chain", "topHoldersPercentOfTotalSupply"),
    "Percent of Token Supply on Exchanges": ("On-chain", "percentOfTokenSupplyOnExchanges"),
    "Realized Value": ("On-chain", "realizedValue"),
    "Market Value To Realized Value": ("On-chain", "mvrvRatio"),
    "NVT Ratio Circulation": ("On-chain", "nvtRatioCirculation"),
    "NVT Ratio Transaction Volume": ("On-chain", "nvtRatioTxVolume"),
    "Network Growth": ("On-chain", "networkGrowth"),
    "Daily Active Addresses": ("On-chain", "dailyActiveAddresses"),
    "Token Age Consumed": ("On-chain", "tokenAgeConsumed"),
    "Token Velocity": ("On-chain", "tokenVelocity"),
    "Transaction Volume": ("On-chain", "transactionVolume"),
    "Token Circulation": ("On-chain", "tokenCirculation"),
}

chart_settings_options = {
    "share": "Share chart",
    "download": "Download as PNG",
}

xpaths_main = {
    "chart_page_element": """//div[@class="ChartPage_wrapper__805jp"]""",
    "period_selector": "//div[contains(@class, 'ChartPage_ranges__3h7wX')]//div[text()='{0}']",
    "period_selector_active": "//div[contains(@class, 'Selector_selected__2rsUx')]",
    "metrics_category": "//button[contains(@class, 'ChartMetricSelector_btn__1PClN')]",
    "metrics_category_active": "//button[contains(text(), '{0}') and contains(@class, 'Button_active__3FPKU')]",
    "metric": """//button[contains(@class, 'ChartMetricSelector_btn__1PClN')]//div[@class="ChartMetricSelector_btn__left__eQVvm"]""",
    "active_metric": "//button[contains(text(), '{0}') and contains(@class, 'ChartActiveMetrics_btn__3bHzp')]",
    "any_active_metric": "//button[contains(@class, 'ChartActiveMetrics_btn__3bHzp')]",
    "inactive_metric": "//span[text()='no data']",
    "search_result": """//button[contains(@class, SearchWithSuggestions_suggestion__AqZNi)]//span[@class="SearchContainer_name__3fYwt"]""",
    "chart_settings_menu_item": "//button[text()='{0}']",
}

selectors_main = {
    "close_cookies_button": "#root div.CookiePopup_wrapper__c_4dc button.CookiePopup_btn__3Jhvd",
    "close_assets_button": "#root div.ChartPage_wrapper__805jp div.Tooltip_tooltip__fE-Ct button.SidecarExplanationTooltip_btn__1xriD",
    "chart_header_element": "div.Header_wrapper__fXGgW",
    "search_dialog": 'div.Dialog_modal__1QXQD.Panel_panel__280Ap',
    "search_input": 'input.Input_input__1XjEb',
    "search_result_list": "div.SearchWithSuggestions_suggestions__3z1wA",
    "close_search_dialog": "svg.Dialog_close__wPN0y",
    "token_selector_element": "#root div.Header_wrapper__fXGgW div.Header_selector__3x1uF",
    "token_image": '#root div.Header_wrapper__fXGgW div.Header_selector__3x1uF div.project-icon',
    "token_title": "#root div.Header_wrapper__fXGgW div.Header_selector__3x1uF div.Header_project__top__1FwRn h1.Header_project__name__2-7uj",
    "token_description": "div.Header_selector__3x1uF div.Header_project__description__3NwC1",
    "token_price": "div.Header_projectInfo__2RVm0 div.Header_column__2kJMx:nth-child(1) div.Header_usdWrapper__1liTy span:first-child",
    "token_price_currency": "div.Header_projectInfo__2RVm0 div.Header_column__2kJMx:nth-child(1) div.Header_usdWrapper__1liTy span.Header_currency__3vx-4",
    "token_volume": "div.Header_projectInfo__2RVm0 div.Header_column__2kJMx:nth-child(1) div:last-child span:first-child",
    "token_volume_currency": "div.Header_projectInfo__2RVm0 div.Header_column__2kJMx:nth-child(1) div:last-child span.Header_currency__3vx-4",
    "add_signal_button": "div.Header_actions__2wTa5 button:nth-child(2)",
    "watch_button": "div.Header_actions__2wTa5 button:nth-child(3)",
    "metrics_menu": "div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n",
    "metrics_menu_title": "div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n div.Panel_header__x1vbc.ChartMetricSelector_header__31oOd",
    "modal_overlay": "div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO",
    "metrics_categories": 'div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_categories__uBPiA',
    "metrics_list": 'div.ChartMetricSelector_group__FhAJt',
    "active_metrics_panel": 'section.ChartActiveMetrics_wrapper__3Z0I8',
    "close_active_metric": 'svg.ChartActiveMetrics_icon__17g9k',
    "share_dialog": 'div.Dialog_modal__1QXQD.Panel_panel__280Ap',
    "share_link": 'input.Input_input__1XjEb.SharePanel_link__input__2bRzG',
    "close_share_dialog": 'svg.Dialog_close__wPN0y',
    "graph_title": 'div.ChartPage_title__fLVYV',
    "calendar_dates": 'button.CalendarBtn_btn__2WS5X',
    "interval": 'div.Dropdown_wrapper__2SIQh.IntervalSelector_wrapper__3_304',
    "metrics_menu_button": "button.ChartMetricsTool_trigger__3DzJE",
    "chart_settings_button": "div.ChartPage_settings__group__p-3hT button.Button_button__16STw.Button_flat__2o9Q6",
    "chart_settings_menu": "div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n",
    "chart_date": "div.recharts-wrapper g.recharts-cartesian-axis-ticks g.recharts-layer.recharts-cartesian-axis-tick:{0}-child tspan",
    "account_menu_button": "header.Navbar_header__ay1vx div.Navbar_right__1MerY div.dd__trigger:nth-child(3) button.Navbar_btn__3ZCA_",
    "account_menu": "#dd-modal div.NavbarProfileDropdown_wrapper__2mpA1",
    "chart_loader": "#root div.ChartPage_wrapper__805jp div.Chart_loader__1bLXA",
}

xpaths_insights = {}

selectors_insights = {
    "close_cookie_popup_button": "body > div.SAN-panel.SAN-panel_context.wrapper.svelte-1ezhlqq > div > button",
    "featured_insights_title": "body > main > div.insights.bot-scroll.svelte-1rgf045 > div.insights__featured.svelte-1rgf045 > h2",
    "write_button": "body > main > div.top.svelte-17jgipm > div > a",
    "tab": "body > main > div.SAN-tabs.tabs.svelte-17jgipm > a.SAN-tab",
    "active_tab": "body > main > div.SAN-tabs.tabs.svelte-17jgipm > a.SAN-tab.active",
    "loader": "body > div.bar.svelte-rgfq4j > div",
    "draft": "body > main > div.insights.bot-scroll.svelte-1czt5h1 > div.SAN-panel.SAN-panel_box wrapper.svelte-1ytyh61",
    "draft_delete_button": "div > div > svg",
    "draft_edit_button": "div > div > a",
    "draft_title": "a.title.svelte-1ytyh61",
    "draft_text": "h4.svelte-1ytyh61",
    "draft_timestamp": "div.bottom.svelte-1ytyh61 > h3.svelte-1ytyh61",
    "insight": "body > main > div.insights.bot-scroll > div.insights__item",
    "insight_title": "div > div > div.top.svelte-s28iwd > a",
    "insight_author": "div > div > div.bottom.svelte-s28iwd > div > div > div > a",
    "insight_timestamp": "div > div > div.bottom.svelte-s28iwd > div > div > div > div",
    "insight_tag": "div > div.left.svelte-vl3i68 > div.top.svelte-s28iwd > div > a",
    "insight_tag_title": "div > div.right.svelte-vl3i68 > h3",
    "insight_like_button": "div > div > div.bottom.svelte-s28iwd > button",
    "editor_title": "#react-mount-node > div > div.InsightEditor-module_insightWrapper__3CQqa > textarea",
    "editor_body": "#react-mount-node > div > div.InsightEditor-module_insightWrapper__3CQqa > div > div > div.DraftEditor-root > div.DraftEditor-editorContainer > div > div > div > div",                   
    "editor_publish_menu_button": "#react-mount-node > div > div.InsightEditor-module_bottom__1VQ3s > div > button",
    "editor_tag_input": "div[id*='react-select-'][id$='--value'] > div.Select-input > input",
    "editor_tag_list_item": "div[id*='react-select-'][id$='--list'] > div:nth-child(1) > div > div > div.VirtualizedSelectOption",
    "editor_selected_tag": "span[id*='react-select-'][id*='--value-']",
    "editor_clear_tags": "body > div.Modal-module_wrapper__3yPRh.ContextMenu-module_wrapper__NSGRk > div.Tooltip-module_tooltip__5Yj1c.ContextMenu-module_menu__3N81H > div > div.Select.Select-module_topDropdown__dOxgi > div > span.Select-clear-zone > span",
    "editor_publish_insight_button": "body > div.Modal-module_wrapper__3yPRh.ContextMenu-module_wrapper__NSGRk > div.Tooltip-module_tooltip__5Yj1c.ContextMenu-module_menu__3N81H > div > button",
    "editor_saved_timestamp": "#react-mount-node > div > div.InsightEditor-module_bottom__1VQ3s > div > span",
    "read_title": "body > main > div > h1",
    "read_body": "body > main > div > div.text.svelte-1j8b64g > p",
    "read_tag": "body > main > div > div.bottom.bot-scroll.svelte-1j8b64g > a",
    "read_author": "body > main > div > div.insight__info.svelte-1j8b64g > div > div.info.svelte-y4lt2b > a",
    "read_timestamp": "body > main > div > div.insight__info.svelte-1j8b64g > div > div.info.svelte-y4lt2b > div",
    "read_follow": "body > main > div > div.insight__info.svelte-1j8b64g > button",
    "read_like_button": "body > main > div > div.bottom.bot-scroll.svelte-1j8b64g > div > div:nth-child(3) > button.svelte-10pde3u",
    "read_share_button": "body > main > div > div.bottom.bot-scroll.svelte-1j8b64g > div > div:nth-child(3) > button.SAN-btn.trigger.info__share.svelte-11gg91w",
    "share_dialog": "body > main > div > div.bottom.bot-scroll.svelte-1j8b64g > div > div:nth-child(3) > div.SAN-panel.SAN-panel_context.dialog.svelte-19nk3mr",
    "share_dialog_close_button": "body > main > div > div.bottom.bot-scroll.svelte-1j8b64g > div > div:nth-child(3) > div.SAN-panel.SAN-panel_context.dialog.svelte-19nk3mr > div.top.svelte-19nk3mr > svg",
}

delta = {
    "1d": (relativedelta(days=1), timedelta(days=1)),
    "1w": (relativedelta(weeks=1), timedelta(days=1)),
    "1m": (relativedelta(months=1), timedelta(days=2)),
    "3m": (relativedelta(months=3), timedelta(days=10)),
    "6m": (relativedelta(months=6), timedelta(days=20)),
    "1y": (relativedelta(years=1), timedelta(days=30)),
    "all": (relativedelta(), timedelta()),
}

bot_url = "https://api-stage.santiment.net/bot/login/"

title_conversion = {
    "Santiment Network Token (SAN)": "Santiment (SAN)",
}

urls = {
    "stage": {
        'main': "https://app-stage.santiment.net/?metrics=historyPrice&slug=bitcoin&title=Bitcoin%20%28BTC%29",
        'insights': 'https://insights-stage.santiment.net',
        'sonar': 'https://app-stage.santiment.net/sonar/my-signals'
    },
    "prod": {
        'main': "https://app.santiment.net/?metrics=historyPrice&slug=bitcoin&title=Bitcoin%20%28BTC%29",
        'insights': 'https://insights.santiment.net',
        'sonar': 'https://app.santiment.net/sonar/my-signals'
    },
}
