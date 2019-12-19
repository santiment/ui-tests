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

delta = {
    "1d": (relativedelta(days=1), timedelta(days=1), '10min'),
    "1w": (relativedelta(weeks=1), timedelta(days=1), '10min'),
    "1m": (relativedelta(months=1), timedelta(days=2), '2h'),
    "3m": (relativedelta(months=3), timedelta(days=10), '12h'),
    "6m": (relativedelta(months=6), timedelta(days=20), '12h'),
    "1y": (relativedelta(years=1), timedelta(days=30), '2d'),
    "all": (relativedelta(), timedelta(), '2d'),
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
