import requests
import json
import glob
import sys, os
import datetime
from discord import Webhook, RequestsWebhookAdapter, File
from constants import DISCORD_WEBHOOK, ENVIRONMENT, CONFIG_FILE, DISCORD_USER_ID

if DISCORD_WEBHOOK:
    baseURL = "https://discordapp.com/api/webhooks/{}".format(DISCORD_WEBHOOK)
    webhook = Webhook.from_url(baseURL, adapter=RequestsWebhookAdapter())

    str_start = sys.argv[1]
    str_finish = sys.argv[2]
    pattern = '%H:%M:%S'
    diff = datetime.datetime.strptime(str_finish, pattern) - datetime.datetime.strptime(str_start, pattern)
    str_diff = str(diff)

    str_start_replaced = str_start.replace(':', '_')
    path_to_report = os.path.join('reports', '*.html')
    files = [File(open(path, 'rb'), os.path.basename(path).replace('.', f'_{ENVIRONMENT}_{CONFIG_FILE}_{str_start_replaced}.')) for path in glob.glob(path_to_report)]

    if ENVIRONMENT == 'stage' and DISCORD_USER_ID:
        mention = f"<@{DISCORD_USER_ID}>"
    else:
        mention = ""

    message = f"""
    ++++++++++++++++++++++++++++++++++++++++++++++
    {mention}
    Test run results:
    Started at {str_start}, finished at {str_finish}
    Total duration: {str_diff}
    Environment: {ENVIRONMENT}
    Config: {CONFIG_FILE}
    ===============================================
    """
    webhook.send(message, username='TestResultsBot', files=files)
