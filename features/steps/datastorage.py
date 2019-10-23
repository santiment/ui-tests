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
    "log": "Log scale",
    "share": "Share chart",
    "download": "Download as PNG",
}

selectors_main = {
    "page_loader_big": "#root > div.loader",
    "page_loader_small": "#root > div > div.page.detailed > div > div.PageLoader_loader__2q97l",
    "close_cookie_popup_button": "#root > div > div.CookiePopup_wrapper__c_4dc > button",
    "close_explore_popup_button": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartSidecar_wrapper__3FE6D > div > div.Tooltip_tooltip__fE-Ct > button",
    "close_signals_popup_button": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.Chart_wrapper__28v4S.ChartPage_chart__34CY1 > div:nth-child(1) > div > div > button",
    "search_dialog": 'body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Panel_panel__280Ap',
    "search_dialog_close": "body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Panel_panel__280Ap > div.Panel_header__x1vbc > svg",
    "search_input": 'body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Panel_panel__280Ap > div.Dialog_content__HslRr > div.SearchWithSuggestions_wrapper__3BM6h > div > input',
    "search_dialog_asset": "body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Panel_panel__280Ap > div.Dialog_content__HslRr > div.TriggerProjectsSelector_contentWrapper__3Hkrb > div > div:nth-child(1) > div > div > div",
    "search_dialog_asset_name": "div > span.ProjectsList_name__PyRBs",
    "search_dialog_asset_ticker": "div > span.Label_label__o8xCv.Label_waterloo__PY2nL",
    "search_result_list": "body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Panel_panel__280Ap > div.Dialog_content__HslRr > div.SearchWithSuggestions_wrapper__3BM6h > div.SearchWithSuggestions_suggestions__3z1wA",
    "search_result_list_no_results": "body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Panel_panel__280Ap > div.Dialog_content__HslRr > div.SearchWithSuggestions_wrapper__3BM6h > div.SearchWithSuggestions_suggestions__3z1wA > div.SearchWithSuggestions_noresults__oTELl",
    "search_result": "body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Panel_panel__280Ap > div.Dialog_content__HslRr > div.SearchWithSuggestions_wrapper__3BM6h > div.SearchWithSuggestions_suggestions__3z1wA > button",
    "search_result_name": "div > div > span.SearchContainer_name__3fYwt",
    "search_result_ticker": "div > div > span.SearchContainer_ticker__3FmLx",
    "chart_header": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW",
    "token_selector": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div:nth-child(1) > div",
    "token_image": '#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div:nth-child(1) > div > div.project-icon',
    "token_title": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div:nth-child(1) > div > div.Header_project__2wmiE > div.Header_project__top__1FwRn > h1",
    "token_description": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div:nth-child(1) > div > div.Header_project__2wmiE > div.Header_project__description__3NwC1",
    "token_price": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div.Header_projectInfo__2RVm0 > div:nth-child(1) > div.Header_usdWrapper__1liTy > span:nth-child(1)",
    "token_price_currency": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div.Header_projectInfo__2RVm0 > div:nth-child(1) > div.Header_usdWrapper__1liTy > span.Header_currency__3vx-4",
    "token_volume": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div.Header_projectInfo__2RVm0 > div:nth-child(1) > div:nth-child(2) > span.Header_totalSupply__I1TPZ",
    "token_volume_currency": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div.Header_projectInfo__2RVm0 > div:nth-child(1) > div:nth-child(2) > span.Header_currency__3vx-4",
    "token_change_24h": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div.Header_projectInfo__2RVm0 > div:nth-child(2) > span:nth-child(2)",
    "token_change_7d": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div.Header_projectInfo__2RVm0 > div:nth-child(3) > span:nth-child(2)",
    "add_signal_button": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div.Header_actions__2wTa5 > button:nth-child(2)",
    "watch_button": "#root > div > div.page.detailed > div:nth-child(1) > div > div.Header_wrapper__fXGgW > div.Header_actions__2wTa5 > button:nth-child(3)",
    "chart_page": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div",
    "chart_loader": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.Chart_wrapper__28v4S.ChartPage_chart__34CY1 > div.Chart_loader__1bLXA",
    "chart_page_settings": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartPage_settings__1k0SP",
    "graph_title": '#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartPage_settings__1k0SP > div:nth-child(1) > h3',
    "period": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartPage_settings__1k0SP > div:nth-child(2) > div.Selector_wrapper__3KsWL.ChartPage_ranges__3h7wX > div",
    "period_active": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartPage_settings__1k0SP > div:nth-child(2) > div.Selector_wrapper__3KsWL.ChartPage_ranges__3h7wX > div.Selector_selected__2rsUx",
    "calendar_button": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartPage_settings__1k0SP > div:nth-child(2) > button.CalendarBtn_btn__2WS5X",
    "interval_button": '#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartPage_settings__1k0SP > div:nth-child(2) > div.IntervalSelector_wrapper__3_304',
    "chart_settings_button": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartPage_settings__1k0SP > div:nth-child(2) > button.Button_flat__2o9Q6",
    "chart_settings_menu": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div",
    "chart_settings_menu_option": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div > button",
    "share_dialog": "body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Dialog_animation__y6vdC.Panel_panel__280Ap",
    "share_dialog_link": "body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Dialog_animation__y6vdC.Panel_panel__280Ap > div.Panel_content__Dg-dF.Dialog_content__HslRr.SharePanel_wrapper__3zjGh > div.SharePanel_content__2duT8 > div:nth-child(1) > input",
    "share_dialog_close": "body > div.Modal_wrapper__3lQw2.Dialog_wrapper__zgx32 > div.Dialog_modal__1QXQD.Dialog_animation__y6vdC.Panel_panel__280Ap > div.Panel_header__x1vbc.Dialog_title__1_fUO.ChartPage_title__fLVYV.Panel_padding__3rWzM > svg",
    "chart_metrics_wrapper": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartMetricsTool_wrapper__1BYzv",
    "metrics_menu_button": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartMetricsTool_wrapper__1BYzv > button",
    "modal_overlay": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Modal_dimmed__27Xzl.ContextMenu_bg__291tK",
    "metrics_menu": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div",
    "metrics_menu_title": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div > div.ChartMetricSelector_header__31oOd",
    "metrics_menu_loader": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div > div.Panel_content__Dg-dF.ChartMetricSelector_wrapper__1PSn4.ChartMetricsTool_selector__2IGIR > div.ChartMetricSelector_loader__1-2NC",
    "metrics_menu_category": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div > div.Panel_content__Dg-dF.ChartMetricSelector_wrapper__1PSn4.ChartMetricsTool_selector__2IGIR > div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_categories__uBPiA > div > button",
    "metrics_menu_category_active": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div > div.Panel_content__Dg-dF.ChartMetricSelector_wrapper__1PSn4.ChartMetricsTool_selector__2IGIR > div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_categories__uBPiA > div > button.Button_active__3FPKU.ChartMetricSelector_active__1FivM",
    "metrics_menu_metric": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div > div.Panel_content__Dg-dF.ChartMetricSelector_wrapper__1PSn4.ChartMetricsTool_selector__2IGIR > div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_metrics__10lIC > div > div > div > button",
    "metrics_menu_metric_selected": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div > div.Panel_content__Dg-dF.ChartMetricSelector_wrapper__1PSn4.ChartMetricsTool_selector__2IGIR > div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_metrics__10lIC > div > div > div > button.Button_active__3FPKU.ChartMetricSelector_active__1FivM",
    "metrics_menu_metric_nodata": "body > div.Modal_wrapper__3lQw2.ContextMenu_wrapper__3VXIO > div.Tooltip_tooltip__fE-Ct.ContextMenu_menu__35C1n > div > div.Panel_content__Dg-dF.ChartMetricSelector_wrapper__1PSn4.ChartMetricsTool_selector__2IGIR > div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_metrics__10lIC > div > div > div > button.Button_disabled__1gOEo.ChartMetricSelector_disabled__2CtQK",
    "metrics_menu_metric_add": "div > div.ChartMetricSelector_btn__action_add__21Na_",
    "metrics_menu_metric_remove": "div > div.ChartMetricSelector_btn__action_remove__1LpCD",
    "active_metric": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.ChartMetricsTool_wrapper__1BYzv > section > button",
    "active_metric_close": 'svg.ChartActiveMetrics_icon__17g9k',
    "general_info": "#root > div > div.page.detailed > div:last-child > div:nth-child(1)",
    "general_info_market_cap": "#root > div > div.page.detailed > div:last-child > div:nth-child(1) > div.PanelWithHeader_content__2zox0 > div > div:nth-child(2) > div.GeneralInfoBlock_value__24ZMc",
    "general_info_price": "#root > div > div.page.detailed > div:last-child > div:nth-child(1) > div.PanelWithHeader_content__2zox0 > div > div:nth-child(3) > div.GeneralInfoBlock_value__24ZMc",
    "general_info_volume": "#root > div > div.page.detailed > div:last-child > div:nth-child(1) > div.PanelWithHeader_content__2zox0 > div > div:nth-child(4) > div.GeneralInfoBlock_value__24ZMc",
    "general_info_supply": "#root > div > div.page.detailed > div:last-child > div:nth-child(1) > div.PanelWithHeader_content__2zox0 > div > div:nth-child(5) > div.GeneralInfoBlock_value__24ZMc",
    "chart_axis_date": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.Chart_wrapper__28v4S.ChartPage_chart__34CY1 > div.recharts-responsive-container > div.recharts-wrapper > svg > g.recharts-layer.recharts-cartesian-axis.recharts-xAxis.xAxis > g > g > text > tspan",
    "chart_axis_value": "#root > div > div.page.detailed > div:nth-child(1) > div > div.ChartPage_wrapper__805jp > div.ChartPage_tool__2vx_W > div > div.Chart_wrapper__28v4S.ChartPage_chart__34CY1 > div.recharts-responsive-container > div.recharts-wrapper > svg > g.recharts-layer.recharts-cartesian-axis.recharts-yAxis.yAxis > g > g > text > tspan",
    "account_menu_button": "#root > div > header > div > div.Navbar_right__1MerY > div:nth-child(3) > button",
    "account_menu": "#dd-modal > div > div.dd__list",
}

selectors_insights = {
    "close_cookie_popup_button": "body > div.SAN-panel.SAN-panel_context.wrapper > div > button",
    "featured_insights_title": "body > main > div.insights.bot-scroll > div.insights__featured > h2",
    "write_button": "body > main > div.top > div > a",
    "tab": "body > main > div.SAN-tabs.tabs > a.SAN-tab",
    "active_tab": "body > main > div.SAN-tabs.tabs > a.SAN-tab.active",
    "loader": "body > div.bar > div",
    "draft": "body > main > div.insights.bot-scroll > div",
    "draft_delete_button": "div > div > svg",
    "draft_edit_button": "div > div > a",
    "draft_title": "a.title",
    "draft_body": "h4",
    "draft_timestamp": "div.bottom > h3:nth-child(1)",
    "draft_delete_dialog": "div > div > div.SAN-panel.SAN-panel_context.dialog",
    "draft_delete_cancel": "div.SAN-dialog__actions.actions > button:nth-child(1)",
    "draft_delete_confirm": "div.SAN-dialog__actions.actions > button:nth-child(2)",
    "insight": "body > main > div.insights div.insights__item",
    "insight_title": "div > div > div.top> a",
    "insight_author": "div > div > div.bottom> div > div > div > a",
    "insight_timestamp": "div > div > div.bottom> div > div > div > div",
    "insight_tag": "div > div.left > div.top> div > a",
    "insight_tag_title": "div > div.right > h3",
    "insight_like_button": "div > div > div.bottom> button",
    "editor_title": "#react-mount-node > div > div.InsightEditor-module_insightWrapper__3CQqa > textarea",
    "editor_body": "#react-mount-node > div > div.InsightEditor-module_insightWrapper__3CQqa > div > div > div.DraftEditor-root > div.DraftEditor-editorContainer > div > div > div > div",
    "editor_publish_menu_button": "#react-mount-node > div > div.InsightEditor-module_bottom__1VQ3s > div button",
    "editor_tag_input": "div[id*='react-select-'][id$='--value'] > div.Select-input > input",
    "editor_tag_list": "div[id*='react-select-'][id$='--list']",
    "editor_tag_list_item": "div[id*='react-select-'][id$='--list'] > div:nth-child(1) > div > div > div.VirtualizedSelectOption",
    "editor_tag_list_toggle": "body > div.Modal-module_wrapper__3yPRh.ContextMenu-module_wrapper__NSGRk > div.Tooltip-module_tooltip__5Yj1c.ContextMenu-module_menu__3N81H > div > div.Select.Select-module_topDropdown__dOxgi.Select--multi > div > span.Select-arrow-zone > span",
    "editor_selected_tag": "span[id*='react-select-'][id*='--value-']",
    "editor_clear_tags": "body > div.Modal-module_wrapper__3yPRh.ContextMenu-module_wrapper__NSGRk > div.Tooltip-module_tooltip__5Yj1c.ContextMenu-module_menu__3N81H > div > div.Select.Select-module_topDropdown__dOxgi > div > span.Select-clear-zone > span",
    "editor_publish_insight_button": "body > div.Modal-module_wrapper__3yPRh.ContextMenu-module_wrapper__NSGRk > div.Tooltip-module_tooltip__5Yj1c.ContextMenu-module_menu__3N81H > div > button",
    "editor_publish_insight_loader": "body > div.Modal-module_wrapper__3yPRh.ContextMenu-module_wrapper__NSGRk > div.Tooltip-module_tooltip__5Yj1c.ContextMenu-module_menu__3N81H > div > button > div",
    "editor_saved_timestamp": "#react-mount-node > div > div.InsightEditor-module_bottom__1VQ3s > div > span",
    "read_title": "body > main > div.insight > h1.title",
    "read_body": "body > main > div > div.text > p",
    "read_tag": "body > main > div > div.bottom.bot-scroll > a",
    "read_author": "body > main > div > div.insight__info > div > div.info > a",
    "read_timestamp": "body > main > div > div.insight__info > div > div.info > div",
    "read_follow_button": "body > main > div > div.insight__info > button",
    "read_like_button": "body > main > div > div.bottom.bot-scroll > div > div:nth-child(3) > button",
    "read_share_button": "body > main > div > div.bottom.bot-scroll > div > div:nth-child(3) > button.SAN-btn.trigger.info__share",
    "share_dialog": "body > main > div > div.bottom.bot-scroll > div > div:nth-child(3) > div.SAN-panel.SAN-panel_context.dialog",
    "share_dialog_close_button": "body > main > div > div.bottom.bot-scroll > div > div:nth-child(3) > div.SAN-panel.SAN-panel_context.dialog > div.top > svg",
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

title_conversion = {
    "Santiment Network Token (SAN)": "Santiment (SAN)",
}

urls = {
    "stage": {
        'main': "https://app-stage.santiment.net/projects/bitcoin/?metrics=historyPrice&slug=bitcoin&title=Bitcoin%20%28BTC%29",
        'insights': 'https://insights-stage.santiment.net',
        'sonar': 'https://app-stage.santiment.net/sonar/my-signals',
        'bot': 'https://api-stage.santiment.net/bot/login/'
    },
    "prod": {
        'main': "https://app.santiment.net/projects/bitcoin/?metrics=historyPrice&slug=bitcoin&title=Bitcoin%20%28BTC%29",
        'insights': 'https://insights.santiment.net',
        'sonar': 'https://app.santiment.net/sonar/my-signals',
        'bot': 'https://api.santiment.net/bot/login/'
    },
}

can_cant = ['can', 'cannot', 'can not', "can't"]
do_dont = ['do', 'do not', "don't"]
have_havent = ['have', 'has', "have not", "has not," "haven't", "hasn't", "don't have", "doesn't have"]
insights_filter_options = ['author', 'first tag']
insights_length_options = ['empty', 'short', 'long']
